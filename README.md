Steps for setting up service rung the following commands:<br>
<ul>
<li> Jupyter notebook has nothing to do with this microservice just shared to explain the experiments I did</li>
<li>pip install -r requirements.txt </li>
<li>mkdir <b>logs</b><br></li>
<li><b>python3 main.py</b></li>
  <li><dl>endpoints:
<dt>get methods: <a>http://localhost:8080/</a>, <a>http://localhost:8080/props</a></dt>
<dt>Post method: <a>http://localhost:8080/matchscore</a></dt>
</dl></li>
<li>Request object:</li>
    <dd>{
    {
    "mentee_major":["Accounting and Financial Management"],
    "mentee_experitse":["Accounting"],
    "mentee_help_topics":[],
    "mentor_major":[],
    "mentor_experitse":["Finance","Accounting"],
    "mentor_help_topics":[]
}</dd>
 <li>Tried <b>supoprt vector classifier</b> as well there isn't much improvement. Lot of <b>False positives</b> are there even I tried removing the data where where both <b>help topic and expertise wrt Mentee and Mentor are missing</b> results only boosed by <b>5% in accuracy</b>.</li>
  <li>Haven't tried filling missing values as each feature has many values either help topics or expertise</li>
</ul>

