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

	def printPKS(self,objects,states_actions,quantifiers):
		
		if len(states_actions)==0: return ""

		output_str = "("

		for (name,arg) in objects:
			if arg.startswith('_'): arg = "xx"+arg[1:]
			output_str += "?"+arg+" : "+name+", "

		if len(output_str)>1: output_str = "(existsK" + output_str[:-2] + ") "

		output_str += "K("

		for (name,args) in states_actions:
			output_str += name+"("
			for arg in args:
				if arg=="H": output_str += "human, "
				elif arg.isupper(): output_str += arg.lower()+", "
				elif arg.startswith('_'): output_str += "?xx"+arg[1:]+", "
				else: output_str += "?"+arg+", "

			if len(args)>0: output_str = output_str[:-2]
			output_str+=") & "

		output_str = output_str[:-2] + "))" 

		# add quantification if available
		if len(quantifiers)>0:
			qstr = ""
			qind = 1
			for (name,args) in quantifiers:
				qstr+="("+name+"("
				for a in args:
					qstr+="?q"+str(qind)+" : "+a.lower()+", "
				qstr = qstr[:-2]+")"
			
			output_str = qstr + output_str
			for i in range(0,len(quantifiers)):
				output_str+=")"

		return output_str

	def multuply_link_preds_objs(self,objects,states_actions,repeats):
		done_vars = []
		full_states_actions=[]
		rel_objs=[]

		# treat lists: multiply predicates having lists as args
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

		for (name,args) in states_actions:
			# multiply preds if needed
			if args[-1] in repeats:
				for i in range(1,repeats[args[-1]]+1):
					rargs = []
					for a in args[:-1]:
						rargs.append(a+str(i))
					full_states_actions.append((name,rargs))
			else:
				full_states_actions.append((name,args[:-1]))


			# find corresponding objects
			for a in args[:-1]:
				if (not (a in done_vars)):
					done_vars.append(a)
					if a in objects:
						repeat=0
						if a in repeats:
							repeat = repeats[a]
						elif objects[a][1][-1] in repeats:
							repeat = repeats[objects[a][1][-1]]

						if repeat==0:
							rel_objs.append((objects[a][0],a))
						else:
							for i in range(1,repeat+1):
								rel_objs.append((objects[a][0],a+str(i)))	

		return (full_states_actions,rel_objs)	

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

		quantifiers=[]

		for h in Hypo:
			goals = []
			world = []
			commands = []
			repeats = {}
			objects = {}

			for (name,args) in Hypo[h]:
				# goals
				if name.startswith('g#'):
					goals.append((name[2:],args))
				# repeats
				elif name.startswith('r#'):
					repeats[args[0]] = int(args[1])
				elif name.startswith('o#'):
					objects[args[0]] = (name[2:],args)
				elif name.startswith('w#'):
					world.append((name[2:],args))
				elif name.startswith('c#'):
					commands.append((name[2:],args))
				elif name.startswith('q#'):
					quantifiers.append((name[2:],args))


			(fgls,gobjs) = self.multuply_link_preds_objs(objects,goals,repeats)
			full_goals+=list(fgls)
			goal_objects+=list(gobjs)

			(fwls,wobjs) = self.multuply_link_preds_objs(objects,world,repeats)
			full_world+=list(fwls)
			world_objects+=list(wobjs)

			(fcds,cobjs) = self.multuply_link_preds_objs(objects,commands,repeats)
			full_commands+=list(fcds)
			command_objects+=list(cobjs)

		data["goal"] = self.printPKS(goal_objects,full_goals,quantifiers)
		data["SOW"] = self.printPKS(world_objects,full_world,[])
		data["actions"] = self.printPKS(command_objects,full_commands,[])
		return data