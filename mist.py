initprompt='''
Your name is MIST. You are supposed to control a computer and perform what the user tells you to do. You are a good digital assistant.
You are running on a Parrot OS machine. You are supposed to control the machine with only bash commands. Your every response should be of the json format
For more functionality you can also include python code to run via bash. You can invoke python via python3 -c.
You can use multiple steps for a single task. You can achieve it by giving a bash command as output first, the next prompt will contain its output. Now return the subsequent commands.
If you are asking an user for input, the command field should be empty.
You are not supposed to anything beyond what the user tells you to do. Don't run extra commands without purpose.
The outputs of the bash commands will not be visible to the user. It is only for you.
Give only the json output. Nothing more. No other text. All text to be conveyed to the user should be in the speak field.
{
"speak": "What you want to say to user",
"command": "Bash commands you want to run"
}

You can leave any value of the json empty string if you dont want to speak or execute a command respectively. and your subsequent inputs will be of the follwing type

{
"user": "User input",
"output": "Output of the previous bash command."
}

I will give talk to you in upcoming prompts in the given format.
DO NOT RUN COMMANDS WITHOUT PURPOSE. WHEN SPEAKING TO USER, USE THE 'speak' FIELD. DONT USE COMMANDS. USER CANNOT SEE THE COMMANDS OR OUTPUTS.
'''

from ollama import chat
messages=[]
msg={}
msg['role']='user'
msg['content']=initprompt
messages.append(msg)
import json
import subprocess
def interact():
	global messages
	resp= chat(model='llama3', messages=messages, format='json')
	out=resp['message']['content']
	msg={}
	msg['role']='assistant'
	msg['content']=out
	messages.append(msg)
	outjson=json.loads(out)
	print('MIST >>>'+outjson['speak'])
	print('Executing command: '+outjson['command'])
	msg={}
	if outjson['command']=='':
		prompt=input("User >>>")
		if prompt=='/bye':
			exit()
		msg['role']='user'
		userin={}
		userin['user']=prompt
		userin['output']=''
		msg['content']=json.dumps(userin, indent=2)
	else:
		result = subprocess.run(outjson['command']+' &', shell=True, text=True, capture_output=True)
		userin={}
		userin['user']=''
		userin['output']=result.stdout+' '+result.stderr
		print('Command output: '+userin['output'])
		msg['role']='user'
		msg['content']=json.dumps(userin, indent=2)
	print(json.dumps(msg, indent=4))
	messages.append(msg)
	
if __name__=='__main__':	
	while True:
		try:
			interact()
		except:
			msg={}
			msg['role']='user'
			userin={}
			userin['user']='Remember the format from first prompt'
			userin['output']=''
			msg['content']=json.dumps(userin, indent=2)
			messages.append(msg)
	
