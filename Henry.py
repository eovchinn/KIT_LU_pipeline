#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contributors:
#   * Katya Ovchinnikova <e.ovchinnikova@gmail.com> (2014)

import json
import re

# English intransitive verb list 
intrans_verbs = ["move-v"]

class HenryWriter(object):
	def __init__(self, texts, appendix_obs):
		self.Hobs= self.createHenryOutput(texts,appendix_obs)

	def createHenryOutput(self, texts, appendix_obs):
		Ostr = ""

		for text in texts:
			name2ind = {}
			pos2var = {}
			verb_prep_ineq = {}
			verb_prep_ineq_counter = 0
			var2noun = {}
			noun_vars = []

			Ostr+="(O (name %s)(^" % text.id
			#Ostr+=appendix_obs
			for prop in text.props:
				p_name = prop[0]
				args = prop[1]

				# fix intrans verbs: if they sec arg is uninstantiated -> remove it
				if ((p_name in intrans_verbs) & (len(args)>2)):
					if args[3].startswith("u"): args = args[:-2]

				Ostr+=" (%s" % p_name
				for a in args:
					Ostr+=" %s" % a
				Ostr+=" :1)"

				# add propositions for the inequality constraints for predicates with the same name: 
				# verbs, adverbs, preps, adjectives, and props without postfix
				if not (p_name.endswith('-n')):
					if (not p_name in name2ind): name2ind[p_name] = []
					name2ind[p_name].append(args[0])
				# all nouns that are with different names are different
				else:
					if (not args[1] in var2noun): var2noun[args[1]] = []
					var2noun[args[1]].append(p_name)
					noun_vars.append(args[1])

				# arguments of verbs and prepositions are different
				if (p_name.endswith('-v') or p_name.endswith('-p')):
					verb_prep_ineq_counter+=1
					verb_prep_ineq[verb_prep_ineq_counter]=args
					

			# add inequality constraints for same preds
			for n in name2ind.keys():
				for i in range(0,len(name2ind[n])):
					for j in range((i+1),len(name2ind[n])):
						x = name2ind[n][i]
						y = name2ind[n][j]
						if (x!=y): Ostr+=" (!= %s %s)" % (x, y)

			# add inequality constraints for args of a verb of prep
			for c in verb_prep_ineq:
				for i in range(0,len(verb_prep_ineq[c])):
					for j in range((i+1),len(verb_prep_ineq[c])):
						x = verb_prep_ineq[c][i]
						y = verb_prep_ineq[c][j]
						if (x!=y): Ostr+=" (!= %s %s)" % (x, y)


			# add inequality constraints for all nouns with different names
			for i in range(0,len(noun_vars)):
				for j in range((i+1),len(noun_vars)):
						x = noun_vars[i]
						y = noun_vars[j]
						if (x!=y) and (not (set(var2noun[x]) & set(var2noun[y]))): 
							Ostr+=" (!= %s %s)" % (x, y) 

			Ostr+=appendix_obs + "))\n"
			
		return Ostr

class HenryReader(object):
	def __init__(self, ifile,mode):
		self.Hypo= self.extractHypotheses(ifile,mode)

	# build dict, such that every var is mapped
	# to a representitive var of the equality class
	def buildEqClasses(self,un_classes):
		eqS = {}

		for uc in un_classes:
			rv = ""
			for v in uc:
				if v.isupper():
					rv = v
					break
				elif (not v.startswith('_'))& (not v.startswith('e')):
					rv = v
			if len(rv)==0: rv = uc[0]

			for v in uc:
				if (v != rv)&(not v.startswith('e')):
					eqS[v]=rv

		return eqS

	# replace vars with representitive vars
	def replaceVars(self,eqS,props):
		rprops = []
		for (name,args) in props:
			rargs = []
			for a in args:
				if a in eqS:
					rargs.append(eqS[a])
				else: rargs.append(a)
			#if (not ((name,rargs) in rprops)):
			rprops.append((name,rargs))

		return rprops


	def parseHypothesesHenry(self,line):
		props = []
		un_classes = []
		split_prop = " ^ "
		split_args = ","
		prop_args_pattern = re.compile('([^\[\(]+)(\((.+)\))?')

		for p in line.split(split_prop):
			PROPmatchObj = prop_args_pattern.match(p)
			if PROPmatchObj:
				if PROPmatchObj.group(1):
					p_name = PROPmatchObj.group(1)
					if PROPmatchObj.group(3): args = PROPmatchObj.group(3).split(split_args)
					else: args = []

					if (p_name == '='): 
						un_classes.append(args)
					elif (p_name != '!='): props.append((p_name,args))

				else: print 'Strange prop: ' + p
			else: print 'Strange prop: ' + p

		props = self.replaceVars(self.buildEqClasses(un_classes),props)

		return props

	def parseHypothesesPhillip(self,literals,unifications):
		props = []
		for p_data in literals:
			p_name = p_data[0]
			if len(p_data)>1: args = p_data[1:]
			else: args = []

			props.append((p_name,args))

		un_classes = []
		for [v1,v2] in unifications:
			found = False
			for uc in un_classes:
				if v1 in uc:
					if v2 not in uc: uc.append(v2)
					found = True
					break
				elif v2 in uc:
					if v1 not in uc: uc.append(v1)
					found = True
					break
			if not found: un_classes.append([v1,v2])

		props = self.replaceVars(self.buildEqClasses(un_classes),props)

		return props

	# remove literals that have been unified
	def remove_unified_literals(self, literalid, toremove):
		literals = []

		for (literal,id) in literalid:
			if id not in toremove: literals.append(literal.split())
		return literals

	def extractHypothesesHenry(self, ifile):
		id = ""
		Hypo =  {}
		h_flag = False
		id_pattern = re.compile('.+target="([^"]+)"')
		id_line_start = "<result-inference"
		for line in ifile:
			if line.startswith(id_line_start):
				IDmatchObj = id_pattern.match(line)
				if IDmatchObj: id = IDmatchObj.group(1)
			elif line.startswith("<hypothesis"):
				h_flag = True
			elif line.startswith("</hypothesis>"):
				h_flag = False
			elif h_flag:
					Hypo[id] = self.parseHypothesesHenry(line)
		return Hypo

	def extractHypothesesPhillip(self, ifile):
		id = ""
		Hypo =  {}
		id_pattern = re.compile('.+name="([^"]+)"')
		un_pattern = re.compile('.+unifier="([^"]+)"')

		id_line_start = "<proofgraph"
		# list of pairs (literal,id)
		literalid = []
		# list of lists of unified vars
		unifications = []
		# literal ids to be removed (because of unification)
		toremove = []

		active_line = 'active="yes"'
		for line in ifile:
			if line.startswith(id_line_start):
				if len(id)>0:
					Hypo[id] = self.parseHypothesesPhillip(self.remove_unified_literals(literalid,toremove),unifications)
				IDmatchObj = id_pattern.match(line)
				if IDmatchObj: id = IDmatchObj.group(1)
				literals = []
				unifications = []
				toremove = []
			elif line.startswith("<literal") and active_line in line:
				literal_str = line.partition('>')[-1].rpartition('<')[0]
				lit_data = literal_str.split('):')
				# equality of variables, 
				# is equal to a unification
				if lit_data[0].startswith("(#="):
					v_data = lit_data[0].split()
					unifications.append([v_data[1],v_data[2]])
				else: literalid.append((lit_data[0][1:],lit_data[1]))
			elif line.startswith("<unification") and active_line in line:
				UNmatchObj = un_pattern.match(line)
				if UNmatchObj: 
					un_strings = UNmatchObj.group(1).split(', ')
					for u in un_strings:
						data = u.split('=')
						v1 = data[0]
						v2 = data[1]
						unifications.append([v1,v2])
					# extract literal id
					istart = line.find('):') + 2
					iend = line.find(' ^',istart)
					toremove.append(line[istart:iend])


		if len(id)>0:
			Hypo[id] = self.parseHypothesesPhillip(self.remove_unified_literals(literalid,toremove),unifications)

		return Hypo

	def extractHypotheses(self, ifile, mode):
		if mode == "h": Hypo = self.extractHypothesesHenry(ifile)
		elif mode == "p": Hypo = self.extractHypothesesPhillip(ifile)	

		return Hypo	