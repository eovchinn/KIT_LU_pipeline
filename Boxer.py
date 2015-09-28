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
prepositions = [
	"abaft",
	"aboard",
	"about",
	"above",
	"absent",
	"across",
	"afore",
	"after",
	"against",
	"along",
	"alongside",
	"amid",
	"amidst",
	"among",
	"amongst",
	"around",
	"as",
	"aside",
	"astride",
	"at",
	"athwart",
	"atop",
	"barring",
	"before",
	"behind",
	"below",
	"beneath",
	"beside",
	"besides",
	"between",
	"betwixt",
	"beyond",
	"but",
	"by",
	"concerning",
	"despite",
	"during",
	"except",
	"excluding",
	"failing",
	"following",
	"for",
	"from",
	"given",
	"in",
	"including",
	"inside",
	"into",
	"lest",
	"like",
	"minus",
	"modulo",
	"near",
	"next",
	"of",
	"off",
	"on",
	"onto",
	"opposite",
	"out",
	"outside",
	"over",
	"pace",
	"past",
	"plus",
	"pro",
	"qua",
	"regarding",
	"round",
	"sans",
	"save",
	"since",
	"than",
	"through",
	"throughout",
	"till",
	"times",
	"to",
	"toward",
	"towards",
	"under",
	"underneath",
	"unlike",
	"until",
	"up",
	"upon",
	"versus",
	"via",
	"vice",
	"with",
	"within",
	"without",
	"worth"
]

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

		text_id = ''
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
						text.human_ids.append(int(els[0]))
					elif(els[3] in ['you','your', 'yours']): text.robot_ids.append(int(els[0]))
					elif(els[3] in ['we','our']): text.joint_ids.append(int(els[0]))
				else: print 'Strange word line: ' + line

			# Parse propositions
			elif line.strip():
				props = line.split(' & ')
				for prop in props:
					#print "======================"
					#print prop
					PROPmatchObj = id_prop_args_pattern.match(prop)

					if PROPmatchObj:
						if (PROPmatchObj.group(1)): prop_ids = [int(s) for s in PROPmatchObj.group(1).split(',')]
						else: prop_ids = [1000]
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
						elif prop_name == 'thing' and prop_ids == [1000]:
							text.robot_vars.append(prop_args[1])
							h_r = True
						elif prop_name == 'armar-n':
							text.robot_vars.append(prop_args[1])
							h_r = True

						if not h_r:
							# check if a predicate is a preposition without postfix
							if not (prop_name.endswith('-v')|prop_name.endswith('-n')|prop_name.endswith('-a')|prop_name.endswith('-p')|prop_name.endswith('-r')):
								prop_name = check_prep(prop_name)

							prop_s = (prop_name, prop_args,min(prop_ids))
							text.props.append(prop_s)

					else: print 'Strange prop: ' + prop

				# sort props according its id
				text.props.sort(key=lambda x: x[2])

				# replace vars with constants H and R
				for i in range(len(text.props)):
					(name,args,pid) = text.props[i]
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
    
