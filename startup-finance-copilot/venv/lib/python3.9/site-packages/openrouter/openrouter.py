from requests import post
import json
import ast

print("Note : if you not set model in Openrouter function, this default value will be set to claude instant 1.1")
class roles:
    USER="user"
    SYSTEM="system"
    ASSISTANT="assistant"

class models:
    class openai:
        gpt35_turbo="openai/gpt-3.5-turbo"
        gpt4o_mini = "openai/gpt-4o-mini-2024-07-18"
    class meta_llama:
        llama_31 = "meta-llama/llama-3.1-8b-instruct"
    class mistral:
        nemo = "aetherwiing/mn-starcannon-12b"
    class anthropic:
        claude_instant = "anthropic/claude-instant-1.1"
    class openchat:
        b7_free="openchat/openchat-7b:free"
    class google:
        palm2_code = "google/palm-2-codechat-bison"
            

class Openrouter:
    def __init__(self,model="anthropic/claude-instant-1.1",system_prompt="You Are UseFull Assistant"):
        self.model = model
        self.system_prompt = system_prompt
        self.messages = [{"role":"system","content":system_prompt}]
    def append_messages(self,role,content):
        self.messages.extend([{'role':role,'content':content}])
    def get_messages(self):
        return self.messages
    def get_messages_from_file(self,file):
        file=open(file,"r")
        content = file.read()
        file.close()
        return json.loads(json.dumps(content))
    def export_messages_to_file(self,file,messages):
        file=open(file,"w")
        file.write(str(messages))
        file.close()
    def set_messages(self,jsondict):
        self.messages = ast.literal_eval(jsondict)
    def clear_messages(self):
        self.messages = [{"role":"system","content":self.system_prompt}]
    def ask_stream(self,text):
        model = self.model
        api="https://openrouter.ai/api/v1/chat/completions"
        head = {
          "authority": "openrouter.ai",
          "method": "POST",
          "path": "/api/v1/chat/completions",
          "scheme": "https",
          
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Baggage": "sentry-environment=vercel-production,sentry-release=7848d4dafe54b9a7a9459a871ee13afcb151f734,sentry-public_key=0ed8429ba9964f3fbba5d6f092ed2c8a,sentry-trace_id=0aaf3eb80b57494490abb7a87300fc3d,sentry-sample_rate=0.01,sentry-sampled=false",
            "Content-Length": "113",
            "Content-Type": "text/plain;charset=UTF-8",
            "Http-Referer": "https://openrouter.ai/chat",
            "Origin": "https://openrouter.ai",
            "Priority": "u=1, i",
            "Referer": "https://openrouter.ai/chat",
            "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sentry-Trace": "0aaf3eb80b57494490abb7a87300fc3d-bb6336568fedfc19-0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "X-Title": "OpenRouter: Chatroom",
            "Cookie":"_ga=GA1.1.2094209149.1723032142; __stripe_mid=237f6f99-4d4d-4049-8de0-2ec8d90003998696b4; __stripe_sid=c6c218c0-4271-4fe2-93b8-66f2ced7b6b6e134aa; __client_uat=1723032253; _ga_R8YZRJS2XN=GS1.1.1723032141.1.1.1723033557.0.0.0; __session_NO6jtgZM=eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yUGlRcWt2UlFlZXB3R3ZrVjFZRDhBb3Q1elIiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwczovL29wZW5yb3V0ZXIuYWkiLCJleHAiOjE3MjMwMzM1NzgsImlhdCI6MTcyMzAzMzUxOCwiaXNzIjoiaHR0cHM6Ly9jbGVyay5vcGVucm91dGVyLmFpIiwibmJmIjoxNzIzMDMzNTA4LCJzaWQiOiJzZXNzXzJrS1ZTTjZkUzFXY1pGY0NVbko4SFB1cWxEeSIsInN1YiI6InVzZXJfMml2bzZSSVJQQTdLTE05MmVxSEd0eFZ0MEdEIn0.b1KEyx5pJ4I9kQpjTAiAAEaN_zoVbe2oiixnLXi1U6mXY4Rb3UTHK5t7LRekD2A__kIpKQYoXMAKvGqv34fj0EihN3UgF0uhFz4XP2XghbrzcymlNOY3rHPsn9rcUFcRc58LMzxfxlOzrdy5jZ89bBm3EZ_ysyeD7wESNT30QF-l9hfvaQgYtTraYLhR1u3mCrqOn3Px9KlrVmtlgI1DgkWD8UNfz9N5sdDvV_2TEdOn3eh8H_jK4t2spP5cCc-Zeu1JMucmng64vvsXXhkC1QkUWmABtbWI0OPhfEQ3RFGxwCXRMoCAc4oaXgHboV6RQ-3NgbDzEJAFvRW8a2cHpg; __session=eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yUGlRcWt2UlFlZXB3R3ZrVjFZRDhBb3Q1elIiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwczovL29wZW5yb3V0ZXIuYWkiLCJleHAiOjE3MjMwMzM1NzgsImlhdCI6MTcyMzAzMzUxOCwiaXNzIjoiaHR0cHM6Ly9jbGVyay5vcGVucm91dGVyLmFpIiwibmJmIjoxNzIzMDMzNTA4LCJzaWQiOiJzZXNzXzJrS1ZTTjZkUzFXY1pGY0NVbko4SFB1cWxEeSIsInN1YiI6InVzZXJfMml2bzZSSVJQQTdLTE05MmVxSEd0eFZ0MEdEIn0.b1KEyx5pJ4I9kQpjTAiAAEaN_zoVbe2oiixnLXi1U6mXY4Rb3UTHK5t7LRekD2A__kIpKQYoXMAKvGqv34fj0EihN3UgF0uhFz4XP2XghbrzcymlNOY3rHPsn9rcUFcRc58LMzxfxlOzrdy5jZ89bBm3EZ_ysyeD7wESNT30QF-l9hfvaQgYtTraYLhR1u3mCrqOn3Px9KlrVmtlgI1DgkWD8UNfz9N5sdDvV_2TEdOn3eh8H_jK4t2spP5cCc-Zeu1JMucmng64vvsXXhkC1QkUWmABtbWI0OPhfEQ3RFGxwCXRMoCAc4oaXgHboV6RQ-3NgbDzEJAFvRW8a2cHpg"
        }
        true=True
        false=False
        data = {"stream":true,"model":model,"messages":self.get_messages(),"max_tokens":0}
        stream = post(api,json=data,headers=head,stream=True)
        for chunk in stream.iter_lines():
            if chunk:
                try:
                    get = chunk.decode().replace("data: ","")
                    yield json.loads(get)["choices"][0]["delta"]["content"]
                except:
                    pass

