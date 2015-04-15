#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contributors:
#   * Katya Ovchinnikova <e.ovchinnikova@gmail.com> (2014)

import json
import re

# English intransitive verb list 
intrans_verbs = {
	"move-v": 1
}

class HenryWriter(object):
	def __init__(self, texts):
		self.Hobs= self.createHenryOutput(texts)

	def createHenryOutput(self, texts):
		Ostr = ""

		for text in texts:
			name2ind = {}
			pos2var = {}
			verb_prep_ineq = {}
			verb_prep_ineq_counter = 0
			noun_vars = []

			Ostr+="(O (name %s)(^" % text.id
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
				# verbs, adverbs, preps and props without postfix
				# if not (p_name.endswith('-n') or p_name.endswith('-a')):
				if (not p_name in name2ind): name2ind[p_name] = []
				name2ind[p_name].append(args[0])

				# arguments of verbs and prepositions are different
				if (p_name.endswith('-v') or p_name.endswith('-p')):
					verb_prep_ineq_counter+=1
					verb_prep_ineq[verb_prep_ineq_counter]=args

				# all nouns are different
				if (p_name.endswith('-n')):
					noun_vars.append(args[1])

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

			# add inequality constraints for all nouns
			for i in range(0,len(noun_vars)):
				for j in range((i+1),len(noun_vars)):
						x = noun_vars[i]
						y = noun_vars[j]
						if (x!=y): Ostr+=" (!= %s %s)" % (x, y) 

			Ostr+="))\n"
			
		return Ostr

class HenryReader(object):
	def __init__(self, ifile):
		self.Hypo= self.extractHypotheses(ifile)

	def buildEqClasses(self,equals):
		eqS = {}
		for el in equals:
			vflag = False
			rv = ""
			for e in equals[el]:
				if e[0].isupper():
					rv = e
					break
				# 'e' is here to fix the wrong parse, when prep phrases are attached to nouns
				elif (not e.startswith('_'))&(not e.startswith('e')):
					rv = e
					vflag = True
				elif (not vflag):
					rv = e 
			
			for e in equals[el]:
				# 'e' is here to fix the wrong parse, when prep phrases are attached to nouns
				if (e != rv)&(not e.startswith('e')):
					eqS[e]=rv

		return eqS

	def replaceVars(self,eqS,props):
		rprops = []
		for (name,args) in props:
			rargs = []
			for a in args:
				if a in eqS:
					rargs.append(eqS[a])
				else: rargs.append(a)
			if (not ((name,rargs) in rprops)):
				rprops.append((name,rargs))

		return rprops

	def parseHypotheses(self,line):
		props = []
		equals = {}
		prop_args_pattern = re.compile('([^\[\(]+)(\((.+)\))?')
		for p in line.split(' ^ '):
			PROPmatchObj = prop_args_pattern.match(p)
			if PROPmatchObj:
				if PROPmatchObj.group(1):
					p_name = PROPmatchObj.group(1)
					if PROPmatchObj.group(3): args = PROPmatchObj.group(3).split(',')
					else: args = []

					if (p_name == '='): 
						for a in args:
							if not a in equals.keys(): equals[a] = []
							equals[a] += args
					elif (p_name != '!='): props.append((p_name,args))

				else: print 'Strange prop: ' + p
			else: print 'Strange prop: ' + p

		props = self.replaceVars(self.buildEqClasses(equals),props)	

		return props

	def extractHypotheses(self, ifile):
		id = ""
		Hypo =  {}
		h_flag = False
		id_pattern = re.compile('.+target="([^"]+)"')

		for line in ifile:
			if line.startswith("<result-inference"):
				IDmatchObj = id_pattern.match(line)
				if IDmatchObj: id = IDmatchObj.group(1)
			elif line.startswith("<hypothesis"):
				h_flag = True
			elif line.startswith("</hypothesis>"):
				h_flag = False
			elif h_flag:
				Hypo[id] = self.parseHypotheses(line)

		return Hypo