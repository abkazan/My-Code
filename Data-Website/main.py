# project: p4
# submitter: abkazan
# partner: none
# hours: 10
import pandas as pd
from flask import Flask, request, jsonify, make_response, Response
import matplotlib.pyplot as plt
import re
import time
import io



app = Flask(__name__)
# df = pd.read_csv("main.csv")

num_subscribed = 0

visited = 0
ip_requests = {}
a_cnt = 0
b_cnt = 0

@app.route('/')
def home():
    global visited
    global a_cnt
    global b_cnt
    with open("index.html") as f:
        html = f.read()
    #version A - regular html
    #print(f"visited: {visited}")
    version_b = "<a href = \"donate.html?from=B\" style = \"color: red\">Click here to donate</a>"
    version_a = "<a href = \"donate.html?from=A\" style = \"color: blue\">Click here to donate</a>"
    if visited < 10:      
        if visited % 2 == 0:
            #version A
            visited += 1
            return html
        else:
            visited += 1
            new_html = html.replace(version_a, version_b)
            return new_html
    else:
        if a_cnt < b_cnt:
            visited += 1
            new_html = html.replace(version_a, version_b)
            return new_html
        else:
            return html
            
    return html
    

@app.route('/browse.html')
def browse():
    df = pd.read_csv('main.csv', nrows = 100)
    header = "Browse"
    html = f"<html><head><h1>{header}</h1></head><body>{df.to_html()}</body></html>"
    #matplotlib.use('Agg')
    return html

@app.route('/browse.json')
def browse_json():
    ip_address = request.remote_addr
    last_request = ip_requests.get(ip_address)
    if last_request and (time.time() - last_request < 60):
        message = 'Too many requests. Please try again later'
        response = make_response(jsonify(message))
        response.status_code = 429
        response.headers['Retry-After'] = '60 seconds'
        return response
    
    ip_requests[ip_address] = time.time()
    
    df = pd.read_csv('main.csv', nrows = 100)
    df = df.to_dict('records')
    return jsonify(df)

@app.route('/visitors.json')
def visitors():
    return jsonify(ip_requests)


@app.route('/email', methods=["POST"])
def email():
    global num_subscribed
    email = str(request.data, "utf-8")
    if len(re.findall(r"^\w+@\w+\.\w{1,3}$", email)) > 0: # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(f"{email}\n") # 2
            #print("we are here after f.write\n\n")
        num_subscribed += 1
        return jsonify(f"thanks, your subscriber number is {num_subscribed}!")
    return jsonify("email invalid. Please try again") # 3

@app.route('/img1.svg')
def img1():
    df = pd.read_csv('main.csv', nrows = 100)
    artists = {}
    for a in df["artist_name"]:
        if a in artists:
            artists[a] += 1
        else:
            artists[a] = 1

    data = {}
    for a in artists:
        if artists[a] >= 3:
            data[a] = artists[a]

    fig, ax = plt.subplots()
    ax.bar(list(data.keys()), list(data.values()))
    ax.set_xlabel('Artist')
    ax.set_title('Artists with 3 or more viral songs in top 100')
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data, rotation=45)
    f = io.StringIO() 
    fig.savefig(f, format="svg")
    plt.close()
    return Response(f.getvalue(), headers={"Content-type": "image/svg+xml"})

@app.route('/img2.svg')
def img2():
    df = pd.read_csv('main.csv', nrows = 100)
    df['danceability'].plot()
    plt.xlabel('Song')
    plt.ylabel('Danceability')
    plt.title('Danceability of Songs')
    f = io.StringIO()
    plt.savefig(f, format='svg')
    plt.close()
    return Response(f.getvalue(), headers={"Content-type": "image/svg+xml"})

@app.route('/img3.svg')
def img3():
    df = pd.read_csv('main.csv', nrows = 100)
    plt.scatter(df['duration_mins'], df['energy'])
    plt.xlabel("Duration in minutes")
    plt.ylabel("Energy level")
    plt.title("Relationship Between a songs Duration and Energy level")
    f = io.StringIO()
    plt.savefig(f, format = 'svg')
    plt.close()
    return Response(f.getvalue(), headers={"Content-type": "image/svg+xml"})
    

@app.route('/donate.html')
def donate():
    global a_cnt
    global b_cnt
    url = request.url
    if url[len(url) - 1] == "A":
        a_cnt += 1
    else:
        b_cnt += 1
    donation_plea = "Please donate because I am a broke college student. It means a lot and your funds will be spent wisely!!!! :))))"
    header = "Donations"
    html = f"<html><head><h1>{header}</h1></head><body>{donation_plea}</body></html>"
    return html


        

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.