#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contributors:
#   * Katya Ovchinnikova <e.ovchinnikova@gmail.com> (2014)

import json
from collections import defaultdict
#import pprint

class PKSGenerator(object):
	def __init__(self, Hypo):
		self.cached = []

		self.data = self.generateOutputStruc(Hypo)

	def printPKS_separate(self,goal_array,quantifiers):
		if len(goal_array) == 0: return ("",[])

		all_goals = []
		all_goal_types = {}
		for goal_struc in goal_array:
			(goal_pks,goal_types) = self.printPKS(goal_struc,quantifiers)
			all_goals.append(goal_pks)
			all_goal_types.update(goal_types)
		return (all_goals,all_goal_types)

	def printPKS(self,goal_struc,quantifiers):
		(states_actions,objects,inequalities) = goal_struc

		if len(states_actions)==0: return ""

		output_str = ""
		exist_counter = 0
		done_vars = []
		goal_types = {}

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
				elif arg[0].isupper(): pred_str += arg.lower()+", "
				elif arg.startswith('_'): 
					linked_arg = "?xx"+arg[1:]
					pred_str += linked_arg+", "
				else: 
					linked_arg = "?"+arg
					pred_str += linked_arg+", "

				if len(linked_arg)>0 and (arg not in done_vars):
					for (name,oarg) in objects:
						if oarg == arg:
							obj_str += linked_arg + " : " + name + ", "
							goal_types[linked_arg] = name
					done_vars.append(arg)
			pred_str = pred_str[:-2] + ")"

			if len(obj_str)>0:
				exist_counter += 1
				output_str += "(existsK(" + obj_str[:-2] + ") " + pred_str + ") & "
			else:
				output_str += pred_str + ") & "

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
				qvar = quantifiers[a]
				qstr+= qvar + " : "+a.lower()+", "
				goal_types[qvar] = a.lower()
			qstr = qstr[:-2]+")"
			
			output_str = qstr + output_str + ")"

		return (output_str,goal_types)


	def multiply_preds_with_lists(self,objects,states_actions):
		result = []

		for (name, args) in states_actions:
			multiplied = False
			for j in range(0,len(args)):
				a=args[j]
				if (a in objects) and (objects[a][0]=="list"):
					multiplied = True
					for la in objects[a][1][1:]:
						gargs=list(args)
						gargs[j]=la
						result.append((name,gargs))
			if not multiplied:
				result.append((name,args))

		return result

	def separate_multuply_link_preds_objs(self,objects,states_actions,repeats):
		result = []

		# treat lists: multiply predicates having lists as args
		states_actions = self.multiply_preds_with_lists(objects,states_actions)

		for sa in states_actions:
			result.append(self.multuply_link_preds_objs(objects,[sa],repeats))

		return result


	def multuply_link_preds_objs(self,objects,states_actions,repeats):
		done_vars = []
		full_states_actions=[]
		rel_objs=[]
		inequalities = []


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

		result = []

		for (name,args) in states:
			state_struc = {}

			neg = False
			if name.startswith("n#"):
				name = name[2:]
				neg = True
			elif args[0] in negations:
				neg = True

			state_struc["type"] = "state"
			state_struc["name"] = name
			state_struc["sign"] = not neg

			sargs = []
			for a in args[1:-1]:
				if a[0].isupper(): sargs.append(a.lower())
				elif a in objects:
					sargs.append(objects[a][0])
			state_struc["args"] = sargs

			result.append(state_struc)

		for (name,args) in locations:
			loc_struc = {}

			neg = False
			if name.startswith("n#"):
				name = name[2:]
				neg = True
			elif args[0] in negations:
				neg = True

			loc_struc["type"] = "loc"
			loc_struc["name"] = name
			loc_struc["sign"] = not neg

			largs = []
			for a in args[1:-1]:
				if a[0].isupper(): largs.append(a.lower())
				elif a in objects:
					largs.append(objects[a][0])
			loc_struc["args"] = largs

			result.append(loc_struc)

		return result

	def assign_prefixes(self,objects,loc_objs):
		real_objects = {}

		for a in objects:
			(name,args) = objects[a]
			if not ((name == "list")|(name.startswith("loc_")|(name.startswith("obj_")))):
				if a in loc_objs:
					real_objects[a] = ("loc_"+name,args)
				else: 
					real_objects[a] = ("obj_"+name,args)
			else:
				real_objects[a] = (name,args)

		return real_objects

	def generate_commands(self,objects,states_actions,mode):	
		commands = []
		states_actions = self.multiply_preds_with_lists(objects,states_actions)

		for (name,args) in states_actions:
			command = {}
			cargs = []
			app = ""

			argind = 0

			for a in args:
				argind+=1
				if a=="H": cargs.append("human")
				elif a=="R": cargs.append("agent")
				elif a.isdigit(): cargs.append(a)
				elif a[0].isupper(): 
					cargs.append(a.lower())
					if argind == 4 and mode == "h" and ((name == "grasp") or (name == "putdown")): 
							app = a[0] + a[1:].lower()
				else:
					# find corresponding objects
					if a in objects:
						cargs.append(objects[a][0])
					# there is no related object
					else:
						if name=="grasp":
							if argind==1: cargs.append("agent")
							elif argind==2: cargs.append("obj_hand")
							elif argind==3: cargs.append("location")
							elif argind==4: cargs.append("obj_all")
						elif name=="putdown":
							if argind==1: cargs.append("agent")
							elif argind==2: cargs.append("obj_hand")
							elif argind==3: cargs.append("location")
							elif argind==4: cargs.append("obj_all")
						elif name=="move":
							if argind==1: cargs.append("agent")
							elif argind==2: cargs.append("location")
							elif argind==3: cargs.append("location")
						elif name=="moveRelative":
							if argind==1: cargs.append("agent")
							elif argind==2: cargs.append("1")
							elif argind==3: cargs.append("direction")
						elif name=="relaxArms":
							if argind==1: cargs.append("agent")
							elif argind==2: cargs.append("obj_arm")
						elif name=="moveArmsToHomePosition":
							if argind==1: cargs.append("agent")
							elif argind==2: cargs.append("obj_arm")

			command["name"] = name + app 
			command["args"] = cargs
			commands.append(command)

		return commands

	def generateOutputStruc(self, Hypo):

		data = defaultdict(dict)

		goals_pks = []
		sows_pks = []
		commands_pks = []
		human_actions_pks = []
		all_goal_types = {}
		all_types = []
		all_action_names = []

		quantifiers={}
		qcount = 0

		recplan = False
		feedback = []

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
			types = {}
			relvars = []

			for (name,args) in Hypo[h]:
				# goals
				if name.startswith('g#'):
					goals.append((name[2:],args))
					relvars += args
				# repeats
				elif name.startswith('r#'):
					if (int(args[1]))>1: repeats[args[0]] = int(args[1])
				# nouns
				elif name.endswith('-n'):
					#if args[1] not in objects:
					objects[args[1]] = (name[:-2],[args[1],""])
					if args[0][0] != 'o':
						types[args[1]] = name
				# things
				elif name=="thing":
					if args[1] not in objects:
						objects[args[1]] = ("all",[args[1],""])
				# lists
				elif name == "list":
					objects[args[0]] = (name,args)
					relvars += args[1:]
				# objects added via inference
				elif name.startswith('o#'):
					if args[1] not in objects:
						objects[args[0]] = (name[2:],args)
						if args[0][0] != 'o':
							types[args[0]] = name
				# locations
				elif name.startswith('l#'):
					if args[0][0] != 'o':
						relvars += args
						locations.append((name[2:],args))
				# states
				elif name.startswith('s#'):
					relvars += args
					states.append((name[2:],args))
				# commands
				elif name.startswith('a#'):
					relvars += args
					if args[0]=="R": commands.append((name[2:],args))
					elif args[0]=="H": human_actions.append((name[2:],args))
				# verbs
				elif name.endswith('-v'):
					if not name[:-2] in all_action_names:
						all_action_names.append(name[:-2])
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
				elif name.startswith('f#'):
					feedback = (name[2:],args[0])

			# collect only relevant types
			for v in types:
				if (types[v] not in all_types) and (v in relvars):
					all_types.append(types[v])

			objects = self.assign_prefixes(objects,loc_objs)

			# Correct generation of the goal
			#(goal_pks,goal_types) += self.printPKS(self.multuply_link_preds_objs(objects,goals,repeats),quantifiers) + ";"
			# all_goal_types.append(goal_types)

			# separate goals for fixing long planning
			(goal_pks,goal_types) = self.printPKS_separate(self.separate_multuply_link_preds_objs(objects,goals,repeats),quantifiers)
			if len(goal_pks)>0:	goals_pks += goal_pks
			all_goal_types.update(goal_types)

			sow_pks = self.generate_SOW(objects,locations,states,negations)
			if len(sow_pks)>0: sows_pks += sow_pks

			command_pks = self.generate_commands(objects,commands,"r")
			if len(command_pks)>0: commands_pks += command_pks

			human_action_pks = self.generate_commands(objects,human_actions,"h")
			if len(human_action_pks)>0: human_actions_pks += human_action_pks


		data["goals"] = goals_pks
		data["SOW"] = sows_pks
		data["commands"] = commands_pks
		data["human_actions"] = human_actions_pks
		data["recognize_plan"] = recplan
		data["goal_types"] = all_goal_types
		data["objects_talked_about"] = all_types
		data["context_words"] = all_action_names

		if len(feedback)>0:
			if feedback[1] in negations: data["feedback"] = (feedback[0],False)
			else: data["feedback"] = (feedback[0],True)
		else:
			data["feedback"] = []

		return data