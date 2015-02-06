#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contributors:
#   * Katya Ovchinnikova <e.ovchinnikova@gmail.com> (2014)

import json
import pprint

class Plan(object):
	def __init__(self, agent, plan):
		self.agent = agent
		self.plan = plan

class HelpReq(object):
	def __init__(self, planp, props):
		self.agent = self.defineObject(planp[1][1],props)
		self.requester = self.defineObject(planp[1][2],props)		
		self.action = self.definePlan(planp[1][3],props)

class Action(object):
	def __init__(self, var,name,agent,args):
		self.var = var
		self.name = name
		self.agent = agent
		self.args = args

class Object(object):
	def __init__(self, var, name, attrs, states):
		self.var = var
		self.name = name
		self.attrs = attrs
		self.states = states

class State(object):
	def __init__(self, var, name, obj):
		self.var = var
		self.name = name
		self.obj = obj

class Classifier(object):
	def __init__(self, Hypo):
		self.cached = []

		self.CS = self.classify(Hypo)	

	def findStates(self,var,states,objects):
		ss = []

		for s in states:
			(name,args) = states[s]

			if (args[1]==var):
				if len(args)==2: ss.append((name,[]))
				elif len(args)==3: ss.append((name,self.findObject(args[2],states,objects),self.findObject(args[2],states,objects)))
				self.cached.append(args[0])
		return ss

	def findState(self,var,states,objects):

		for s in states:
			(name,args) = states[s]
			if (args[0]==var):
				self.cached.append(args[0])
				if len(args)==2: return(name,self.findObject(args[1],states,objects))
				elif len(args)==3: return (name,self.findObject(args[1],states,objects),self.findObject(args[2],states,objects))
				return None
		return None

	def findStateBare(self,name,args,objects):

		if len(args)==2: return(name,self.findObjectNoState(args[1],objects))
		elif len(args)==3: return (name,self.findObjectNoState(args[1],objects),self.findObjectNoState(args[2],objects))

		return None

	def findObject(self,var,states,objects):
		if var.isupper(): return [var]

		if not (var in objects): return None

		objs = []

		for (name,args) in objects[var]:
			if (name == "list"):
				for v in args[1:]:
					objs.append(self.findObject(v,states,objects))
			else:
				states = self.findStates(var,states,objects)
				objs.append((name,states))

		return objs

	def findObjectNoState(self,var,objects):
		if var.isupper(): return [var]

		if not (var in objects): return None

		objs = []

		for (name,args) in objects[var]:
			if (name == "list"):
				for v in args[1:]:
					objs.append(self.findObject(v,states,objects))
			else:
				objs.append((name,[]))

		return objs

	def findAction(self,var,actions,states,objects):
		if not (var in actions): return None

		self.cached.append(var)

		objs = []
		(name,args) = actions[var]
		for a in args[1:]:
			objs.append(self.findObject(a,states,objects))
		return (name,objs)


	def findHelp(self,var,helps,actions,states,objects):
		if not (var in helps): return None

		self.cached.append(var)

		helper = self.findObject(helps[var][1],states,objects)
		requester = self.findObject(helps[var][3],states,objects)

		a = self.findAction(helps[var][2],actions,states,objects)
		if a is not None: return ("action",helper,a,requester)

		s = self.findState(helps[var][2],states,objects)
		if s is not None: return ("state",helper,s,requester)

		if helper or requester: return ("NA",helper,None,requester)

		return None

	def findPlan(self,args,helps,actions,states,objects):
		agent = self.findObject(args[1],states,objects)

		h = self.findHelp(args[2],helps,actions,states,objects)
		if h is not None: return ("help", agent,h)

		a = self.findAction(args[2],actions,states,objects)
		if a is not None: return ("action",agent,a)

		s = self.findState(args[2],states,objects)
		if s is not None: return ("state",agent,s)

		if agent is not None: return ("NA",agent,None)

		return None


	def classify(self, Hypo):
		CS = {}
		CS["plans"] = []
		CS["helpRequests"] = []
		CS["actionRequests"] = []
		CS["jointActionRequests"] = []
		CS["humanHelp"] = []		
		CS["humanActions"] = []
		CS["SOA"] = []


		for h in Hypo:
			#print Hypo[h]
			self.cached = []
			planP = []
			helpP = {}
			actionP = {}
			stateP = {}
			objectP = {}

			for (name,args) in Hypo[h]:
				if name.startswith('p#'):
					planP.append(args)
				# help indicator
				elif name.startswith('h#'):
					helpP[args[0]] = args
				# actions
				elif name.startswith('a#'):
					actionP[args[0]] = (name[2:],args)
				# states
				elif name.startswith('s#'):
					stateP[args[0]] = (name[2:],args)
				# objects
				elif name.startswith('o#'):
					if not (args[0] in objectP): objectP[args[0]] = []
					objectP[args[0]].append((name[2:],args))

			# process plans
			for args in planP:
				# if the planner is HR then classify it as joint action request, not plan
				if args[1]=="HR":
					CS["jointActionRequests"].append(self.findAction(args[2],actionP,stateP,objectP))
				else:
					CS["plans"].append(self.findPlan(args,helpP,actionP,stateP,objectP))

			# process help predicates
			for h in helpP:
				args = helpP[h]
				if not args[0] in self.cached:
					# if HUMAN is the agent of help then classify it as human help, not help request
					if args[1]=="H":
						CS["humanHelp"].append(self.findHelp(args[0],helpP,actionP,stateP,objectP))
					else:
						CS["helpRequests"].append(self.findHelp(args[0],helpP,actionP,stateP,objectP))

			# process actions
			for a in actionP:
				(name,args) = actionP[a]
				if not args[0] in self.cached:
					# if HUMAN is the agent of action then classify it as human action
					if args[1]=="H":
						CS["humanActions"].append(self.findAction(args[0],actionP,stateP,objectP))
					# if ROBOT is the agent of action then classify it as action request
					elif args[1]=="R":
						CS["actionRequests"].append(self.findAction(args[0],actionP,stateP,objectP))
					# if HUMAN and ROBOT are the agents of action then classify it as joint action request
					elif args[1]=="HR":
						CS["jointActionRequests"].append(self.findAction(args[0],actionP,stateP,objectP))
					# else classify it as SOA
					else:
						CS["SOA"].append(self.findAction(args[0],actionP,stateP,objectP))

			# process states
			for s in stateP:
				(name,args) = stateP[s]
				if not args[0] in self.cached:
					CS["SOA"].append(self.findStateBare(name,args,objectP))



			#print "PLANS"
			#print json.dumps(planP)
			#print "HELP"
			#print json.dumps(helpP)
			#print "ACTIONS"
			#print json.dumps(actionP)
			#print "STATES"
			#print json.dumps(stateP)
			#print "OBJECTS"
			#print json.dumps(objectP)


		#pprint.pprint(CS, width=1)

		return CS