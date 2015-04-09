#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contributors:
#   * Katya Ovchinnikova <e.ovchinnikova@gmail.com> (2014)

import json
import pprint

class PKSGenerator(object):
	def __init__(self, Hypo):
		self.cached = []

		self.data = self.generatePKS(Hypo)

	def printPKS_separate(self,goal_array,quantifiers):
		all_goals = ""
		for (fgls,gobjs,gineq) in goal_array:
			all_goals += self.printPKS(gobjs,fgls,quantifiers,gineq)+";"
		return all_goals[:-1]

	def printPKS(self,objects,states_actions,quantifiers,inequalities):
		if len(states_actions)==0: return ""

		output_str = ""
		exist_counter = 0

		for (name,args) in states_actions:
			pred_str = ""
			obj_str = ""
			linked_arg = ""

			if name.startswith("n#"): 
				name = name[2:]
				pred_str +=  "!"
			pred_str += "K("+name+"("
			for arg in args:
				if arg=="H": pred_str += "human, "
				elif arg=="R": pred_str += "agent, "
				elif arg in quantifiers: pred_str += quantifiers[arg]+", "
				elif arg[0].isupper():	pred_str += arg+", "
				elif arg.startswith('_'): 
					pred_str += "?xx"+arg[1:]+", "
					linked_arg = "?xx"+arg[1:]
				else: 
					pred_str += "?"+arg+", "
					linked_arg = "?"+arg

				if len(linked_arg)>0:
					for (name,oarg) in objects:
						if oarg == arg:
							obj_str += linked_arg + " : " + name + ", "
			pred_str = pred_str[:-2] + ")"

			if len(obj_str)>0:
				exist_counter += 1
				output_str += "(existsK(" + obj_str[:-2] + ") " + pred_str + ") & "

		# Generate inequalities
		ineqstr = ""
		for ineq in inequalities:
			for i in range(0,len(ineq)):
				if ineq[i].startswith('_'): a1 = "?xx"+ineq[i][1:]
				else: a1 = ineq[i]
				for j in range(i+1,len(ineq)):
					if ineq[j].startswith('_'): a2 = "?xx"+ineq[j][1:]
					else: a2 = ineq[j]
					ineqstr += "K("+a1+" != "+a2+") & "	
		output_str += ineqstr

		output_str = output_str[:-3]

		for i in range(0,exist_counter):
			output_str += ")"

		# add quantification if available
		if len(quantifiers)>0:
			qstr = ""
			qstr+="(forallK("
			for a in quantifiers:
				qstr+=quantifiers[a]+" : "+a.lower()+", "
			qstr = qstr[:-2]+")"
			
			output_str = qstr + output_str + ")"

		return output_str


	def multiply_preds_with_lists(self,objects,states_actions):
		for i in xrange(len(states_actions) - 1, -1, -1):
			(name, args) = states_actions[i]
			for j in range(0,len(args)):
				a=args[j]
				if (a in objects) and (objects[a][0]=="list"):
					del states_actions[i]
					for la in objects[a][1][1:]:
						gargs=list(args)
						gargs[j]=la
						states_actions.append((name,gargs))
		return states_actions

	def separate_multuply_link_preds_objs(self,objects,states_actions,repeats):
		result = []
		for sa in states_actions:
			result.append(self.multuply_link_preds_objs(objects,[sa],repeats))
		return result


	def multuply_link_preds_objs(self,objects,states_actions,repeats):
		done_vars = []
		full_states_actions=[]
		rel_objs=[]
		inequalities = []

		# treat lists: multiply predicates having lists as args
		states_actions = self.multiply_preds_with_lists(objects,states_actions)

		for (name,args) in states_actions:
			# multiply preds if needed
			if args[-1] in repeats:
				for i in range(1,repeats[args[-1]]+1):
					rargs = []
					for a in args[:-1]:
						if (a in objects) and ((a in repeats) or (objects[a][1][-1] in repeats)):
								rargs.append(a+str(i))
						else:
							rargs.append(a)
					full_states_actions.append((name,rargs))
			else:
				full_states_actions.append((name,args[:-1]))


			# find corresponding objects
			for a in args[:-1]:
				if (not (a in done_vars)):
					done_vars.append(a)
					if a in objects:
						repeat=0
						if (a in repeats) or (objects[a][1][-1] in repeats):
							if a in repeats: repeat = repeats[a]
							else: repeat = repeats[objects[a][1][-1]]
							ineqset = []
							for i in range(1,repeat+1):
								rel_objs.append((objects[a][0],a+str(i)))
								ineqset.append(a+str(i))
							inequalities.append(ineqset)
						else:
							rel_objs.append((objects[a][0],a))
						
		return (full_states_actions,rel_objs,inequalities)

	def generate_SOW(self,objects,locations,states,negations):	
		locations = self.multiply_preds_with_lists(objects,locations)
		states = self.multiply_preds_with_lists(objects,states)

		result = ""

		for (name,args) in states:
			neg = False
			if name.startswith("n#"):
				name = name[2:]
				neg = True
			elif args[0] in negations:
				neg = True

			result += "state,"+str(not neg)+","+name
			for a in args[1:-1]:
				if a[0].isupper(): result += ","+a
				elif a in objects:
					result += ","+objects[a][0]
			result += ";"

		for (name,args) in locations:
			neg = False
			if name.startswith("n#"):
				name = name[2:]
				neg = True
			elif args[0] in negations:
				neg = True

			result += "loc,"+str(not neg)+","+name
			for a in args[1:-1]:
				if a[0].isupper(): result += ","+a
				elif a in objects:
					result += ","+objects[a][0]
			result += ";"

		return result[:-1]

	def assign_prefixes(self,objects,loc_objs):
		real_objects = {}

		for a in objects:
			(name,args) = objects[a]
			if not ((name == "list")|(name.startswith("loc_"))):
				if a in loc_objs:
					real_objects[a] = ("loc_"+name,args)
				else: 
					real_objects[a] = ("obj_"+name,args)
			else:
				real_objects[a] = (name,args)

		return real_objects

	def generate_commands(self,objects,states_actions,mode):	
		commands = ''

		for (name,args) in states_actions:
			command = name
			argind = 0
			#if mode == "h": command+="("
			#else: command+=","
			command+=","

			for a in args:
				argind+=1
				if a=="H": command+="human,"
				elif a=="R": command+="agent,"
				elif a[0].isupper(): command+=a+","
				else:
					# find corresponding objects
					if a in objects:
						command+=objects[a][0]+","
					# there is no related object
					else:
						if name=="grasp":
							if argind==1: command+="agent,"
							elif argind==2: command+="obj_hand,"
							elif argind==3: command+="location,"
							elif argind==4: command+="obj_object,"
						elif name=="putdown":
							if argind==1: command+="agent,"
							elif argind==2: command+="obj_hand,"
							elif argind==3: command+="location,"
							elif argind==4: command+="obj_object,"
						elif name=="move":
							if argind==1: command+="agent,"
							elif argind==2: command+="location,"
							elif argind==3: command+="location,"
			#if mode == "h": commands=command[:-1]+"),"
			#else: commands=command[:-1]+";"
			commands+=command[:-1]+";"
		return commands[:-1]

	def generatePKS(self, Hypo):
		data = {}
		data["SOW"] = ""
		data["goal"] = ""

		full_goals=[]
		full_world=[]
		full_commands=[]

		goal_objects=[]
		world_objects=[]
		command_objects=[]

		quantifiers={}
		qcount = 0

		recplan = False

		for h in Hypo:
			goals = []
			world = []
			locations = []
			loc_objs = []
			states = []
			commands = []
			human_actions = []
			repeats = {}
			objects = {}
			negations = []

			for (name,args) in Hypo[h]:
				# goals
				if name.startswith('g#'):
					goals.append((name[2:],args))
				# repeats
				elif name.startswith('r#'):
					repeats[args[0]] = int(args[1])
				# nouns
				elif name.endswith('-n'):
					objects[args[1]] = (name[:-2],[args[1],""])
				# objects added via inference
				elif name.startswith('o#'):
					objects[args[0]] = (name[2:],args)
				# locations
				elif name.startswith('l#'):
					locations.append((name[2:],args))
				# states
				elif name.startswith('s#'):
					states.append((name[2:],args))
				# commands
				elif name.startswith('a#'):
					if args[0]=="R": commands.append((name[2:],args))
					elif args[0]=="H": human_actions.append((name[2:],args))
				# quantifiers
				elif name.startswith('q#'):
					qcount += 1
					quantifiers[args[0]] = "?q"+str(qcount)
				# negations
				elif name == "not":
					negations.append(args[1])
				# location objects
				elif name == "loc":
					loc_objs.append(args[0])
				elif name == "RP":
					recplan = True

			objects = self.assign_prefixes(objects,loc_objs)

			# Correct generation of the goal
			#(fgls,gobjs,gineq) = self.multuply_link_preds_objs(objects,goals,repeats)
			#full_goals+=list(fgls)
			#goal_objects+=list(gobjs)
			#goal = self.printPKS(goal_objects,full_goals,quantifiers,gineq)

			# separate goals for fixing long planning
			goal = self.printPKS_separate(self.separate_multuply_link_preds_objs(objects,goals,repeats),quantifiers)


			sow = self.generate_SOW(objects,locations,states,negations)

			commands = self.generate_commands(objects,commands,"r")
			human_actions = self.generate_commands(objects,human_actions,"h")


		data["goal"] = goal
		data["SOW"] = sow
		data["commands"] = commands
		data["human_actions"] = human_actions
		data["recognize_plan"] = str(recplan)

		return data