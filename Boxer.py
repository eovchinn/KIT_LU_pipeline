#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contributors:
#   * Katya Ovchinnikova <e.ovchinnikova@gmail.com> (2014)

import re
#import json

#class Prop(object):
#	def __init__(self, name, args):
#		self.ids = ids
#		self.name = name
#		self.pos = pos
#		self.args = args

# English preposition list 
prepositions = {
	"abaft": 1,
	"aboard": 1,
	"about": 1,
	"above": 1,
	"absent": 1,
	"across": 1,
	"afore": 1,
	"after": 1,
	"against": 1,
	"along": 1,
	"alongside": 1,
	"amid": 1,
	"amidst": 1,
	"among": 1,
	"amongst": 1,
	"around": 1,
	"as": 1,
	"aside": 1,
	"astride": 1,
	"at": 1,
	"athwart": 1,
	"atop": 1,
	"barring": 1,
	"before": 1,
	"behind": 1,
	"below": 1,
	"beneath": 1,
	"beside": 1,
	"besides": 1,
	"between": 1,
	"betwixt": 1,
	"beyond": 1,
	"but": 1,
	"by": 1,
	"concerning": 1,
	"despite": 1,
	"during": 1,
	"except": 1,
	"excluding": 1,
	"failing": 1,
	"following": 1,
	"for": 1,
	"from": 1,
	"given": 1,
	"in": 1,
	"including": 1,
	"inside": 1,
	"into": 1,
	"lest": 1,
	"like": 1,
	"minus": 1,
	"modulo": 1,
	"near": 1,
	"next": 1,
	"of": 1,
	"off": 1,
	"on": 1,
	"onto": 1,
	"opposite": 1,
	"out": 1,
	"outside": 1,
	"over": 1,
	"pace": 1,
	"past": 1,
	"plus": 1,
	"pro": 1,
	"qua": 1,
	"regarding": 1,
	"round": 1,
	"sans": 1,
	"save": 1,
	"since": 1,
	"than": 1,
	"through": 1,
	"throughout": 1,
	"till": 1,
	"times": 1,
	"to": 1,
	"toward": 1,
	"towards": 1,
	"under": 1,
	"underneath": 1,
	"unlike": 1,
	"until": 1,
	"up": 1,
	"upon": 1,
	"versus": 1,
	"via": 1,
	"vice": 1,
	"with": 1,
	"within": 1,
	"without": 1,
	"worth": 1}

# Check if a predicate is a preposition
def check_prep(pred):
	if pred in prepositions: 
		return pred+'-p'
	return pred

class Text(object):
	def __init__(self, id):
		self.id = id
		self.human_ids = []
		self.robot_ids = []
		self.joint_ids = []
		self.human_vars = []
		self.robot_vars = []
		self.joint_vars = []

		self.props = []

class BoxerReader(object):
	def __init__(self, ifile):
		self.texts = self.parseBoxerOutput(ifile)

		#for text in self.texts:
		#	print text.props
		#self.classifyProps(self.texts)
	
	#def classifyProps(self, texts):
	#	Hactions = []
	#	Ractions = []
	#	helpReq = []
	#	states = []
	
	def parseBoxerOutput(self, ifile):
		texts = []

		# Pattern for parsing: [word id list]:pred_name(arg list)
		id_prop_args_pattern = re.compile('\[([^\]]*)\]:([^\[\(]+)(\((.+)\))?')
		# Pattern for parsing: pred_name_base-postfix
		#prop_name_pattern = re.compile('(.+)-([nvarp])$')
		# Pattern for parsing: id(sentence_id,..) 
		text_id_pattern = re.compile('id\((.+),.+\)')

		for line in ifile:
			# Ignore commented strings		
			if line.startswith('%'): continue
			# Define sentence id
			elif line.startswith('id('): 
				TIDmatchObj = text_id_pattern.match(line)
				if TIDmatchObj:
					text_id = TIDmatchObj.group(1)
					text = Text(text_id) 
				#else: print 'Strange sent id: ' + line
			# Ignore lemmatized word list
			elif line[0].isdigit(): 
				#print line
				els = line.split()
				if(len(els)==5): 
					if(els[3] in ['I','my','mine']): 
						text.human_ids.append(els[0])
					elif(els[3] in ['you','your', 'yours']): text.robot_ids.append(els[0])
					elif(els[3] in ['we','our']): text.joint_ids.append(els[0])
				else: print 'Strange word line: ' + line

			# Parse propositions
			elif line.strip():
				props = line.split(' & ')
				for prop in props:
					#print "======================"
					#print prop
					PROPmatchObj = id_prop_args_pattern.match(prop)

					if PROPmatchObj:
						if (PROPmatchObj.group(1)): prop_ids = PROPmatchObj.group(1).split(',')
						else: prop_ids = []
						prop_name = PROPmatchObj.group(2)
						prop_args = PROPmatchObj.group(4).split(',')

						#prop_s = Prop(prop_ids,prop_name,prop_args)

						# check if prop id is a HUMAN or ROBOT
						h_r = False
						if (set(prop_ids) & set(text.human_ids)):
							text.human_vars.append(prop_args[1])
							h_r = True
						elif (set(prop_ids) & set(text.robot_ids)):
							text.robot_vars.append(prop_args[1])
							h_r = True
						elif (set(prop_ids) & set(text.joint_ids)):
							text.joint_vars.append(prop_args[1])
							h_r = True
						elif ((len(prop_ids)==0) & (prop_name == 'thing')):
							text.robot_vars.append(prop_args[1])
							h_r = True

						if not h_r:
							# check if a predicate is a preposition without postfix
							if not (prop_name.endswith('-v')|prop_name.endswith('-n')|prop_name.endswith('-a')|prop_name.endswith('-p')|prop_name.endswith('-r')):
								prop_name = check_prep(prop_name)

							prop_s = (prop_name, prop_args)
							text.props.append(prop_s)

					else: print 'Strange prop: ' + prop

				# replace vars with constants H and R
				for i in range(len(text.props)):
					(name,args) = text.props[i]
					rargs = []
					for a in args:
						if a in text.human_vars:
							rargs.append('H')
						elif a in text.robot_vars:
							rargs.append('R')
						elif a in text.joint_vars:
							rargs.append('HR')
						else: rargs.append(a)
					text.props[i] = (name,rargs)

				texts.append(text)

		#for text in texts:
		#	print text.id
		#	print text.human_vars
		#	print text.robot_vars
		#	print text.props
			#for prop in text.props:
			#	print prop.name 
			#	print prop.args

		return texts
    
