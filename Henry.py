#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contributors:
#   * Katya Ovchinnikova <e.ovchinnikova@gmail.com> (2014)

import json
import re

class HenryWriter(object):
	def __init__(self, texts):
		self.Hobs= self.createHenryOutput(texts)

	def createHenryOutput(self, texts):
		Ostr = ""

		for text in texts:
			name2ind = {}
			Ostr+="(O (name %s)(^" % text.id
			for prop in text.props:
				Ostr+=" (%s" % prop[0]
				for a in prop[1]:
					Ostr+=" %s" % a
				Ostr+=" :1)"

				# add propositions for the inequality constraints for verbs, preps and props without postfix
				if not ((prop[0].endswith('-n'))|(prop[0].endswith('-a')|(prop[0].endswith('-r')))):
					if (not prop[0] in name2ind): name2ind[prop[0]] = []
					name2ind[prop[0]].append(prop[1][0])

			# add inequality constraints
			for n in name2ind.keys():
				for i in range(0,len(name2ind[n])):
					for j in range((i+1),len(name2ind[n])):
						x = name2ind[n][i]
						y = name2ind[n][j]
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
			for e in el:
				if e[0].isupper():
					rv = e
					break
				elif (not e.startswith('_')):
					rv = e
					vflag = True
				elif (not vflag):
					rv = e 
			
			for e in el:
				if e != rv:
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
		equals = []
		prop_args_pattern = re.compile('([^\[\(]+)(\((.+)\))?')
		for p in line.split(' ^ '):
			PROPmatchObj = prop_args_pattern.match(p)
			if PROPmatchObj:
				if PROPmatchObj.group(1):
					p_name = PROPmatchObj.group(1)
					if PROPmatchObj.group(3): args = PROPmatchObj.group(3).split(',')
					else: args = []
					if (p_name == '='): equals.append(args)
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

		#print json.dumps(Hypo)
		return Hypo