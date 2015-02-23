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

		for (name,args) in states_actions:
			if name.startswith("n#"): 
				name = name[2:]
				output_str +=  "!"
			output_str += "K("+name+"("
			for arg in args:
				if arg=="H": output_str += "human, "
				elif arg in quantifiers: output_str += quantifiers[arg]+", "
				elif arg.isupper(): output_str += arg.lower()+", "
				elif arg.startswith('_'): output_str += "?xx"+arg[1:]+", "
				else: output_str += "?"+arg+", "

			if len(args)>0: output_str = output_str[:-2]
			output_str+=")) & "

		output_str = output_str[:-3] + ")" 

		# add quantification if available
		if len(quantifiers)>0:
			qstr = ""
			qstr+="(forallK("
			for a in quantifiers:
				qstr+=quantifiers[a]+" : "+a.lower()+", "
			qstr = qstr[:-2]+")"
			
			output_str = qstr + output_str + ")"

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
						if (a in objects) and ((a in repeats) or (objects[a][1][-1] in repeats)):
								rargs.append(objects[a][0].upper()+str(i))
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
							continue
						else:
							rel_objs.append((objects[a][0],a))
						
		return (full_states_actions,rel_objs)

	def generate_commands(self,objects,states_actions):	
		commands = ''

		for (name,args) in states_actions:
			command = name
			argind = 0
			for a in args:
				argind+=1
				if a=="H": command+=",human"
				elif a=="R": command+=",robot"
				elif a.isupper(): command+=","+a.lower()
				else:
					# find corresponding objects
					if a in objects:
						command+=","+objects[a][0]
					# there is no related object
					else:
						if name=="grasp":
							if argind==1: command+=",robot"
							elif argind==2: command+=",hand"
							elif argind==3: command+=",location"
							elif argind==4: command+=",object"
						elif name=="putdown":
							if argind==1: command+=",robot"
							elif argind==2: command+=",hand"
							elif argind==3: command+=",location"
							elif argind==4: command+=",object"
						elif name=="move":
							if argind==1: command+=",robot"
							elif argind==2: command+=",location"
							elif argind==3: command+=",location"
			commands+=command+';'
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
				elif name.startswith('s#'):
					world.append((name[2:],args))
				elif name.startswith('c#'):
					commands.append((name[2:],args))
				elif name.startswith('q#'):
					qcount += 1
					quantifiers[args[0]] = "?q"+str(qcount)
					#quantifiers.append((name[2:],(args[0],"?q"+str(qcount)))

			(fgls,gobjs) = self.multuply_link_preds_objs(objects,goals,repeats)
			full_goals+=list(fgls)
			goal_objects+=list(gobjs)

			(fwls,wobjs) = self.multuply_link_preds_objs(objects,world,repeats)
			full_world+=list(fwls)
			world_objects+=list(wobjs)

			commands = self.generate_commands(objects,commands)

		data["goal"] = self.printPKS(goal_objects,full_goals,quantifiers)
		data["SOW"] = self.printPKS(world_objects,full_world,[])
		data["actions"] = commands
		return data