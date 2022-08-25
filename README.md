<center><b><h2>Knowledge-Based Grocery Bagging System</h2></b></center>

<b><h3>Instruction</h3></b>

Navigate into <code>src</code> folder directory <br/>

Install Rich library via <code>pip install Rich</code> <br/>
This program uses Rich libray (https://rich.readthedocs.io/en/stable/) <br/>

Type <code>python3 main.py</code> to start the program

---
<b><h3>Grocery Bagging</h3></b>

<b> 1) Grouping Items: </b> <br/>
Separate items based on their food type. There are four types of separation: Meat & Seafood, Frozen, Food, Non-food  <br/><br/>

<b> 2) Estimating the Number of Bags </b> <br/>
Calculate the estimated bags for items based on the following calculation: <br/>
<code> Number of Bags = Max (⌈ Total Volume / Bag Volume Capacity ⌉, ⌈ Total Weight / Bag Weight Capacity ⌉) </code> <br/><br/>

<b> 3) Sorting Items: <br/>
Sort items according to the item points to heuristicly approximate the order in which humans would have used. Item points are calculated by taking the weighted sum of item properties: <br/>
<center> <code> Item point = 𝑝1𝑤1 + 𝑝2𝑤2 + 𝑝3𝑤3 </code></center> </br>
<center> where <code>𝑝1</code>, <code>𝑝2</code>, <code>𝑝3</code> are the value of item property and <code>𝑤1</code>, <code>𝑤2</code>, <code>𝑤3</code> are the weight of property respectively </center> <br/>
Typically items are ordered from larger, heavier, and more rigid to smaller, lighter, and less rigid. <br/><br/>

<b> 4) Districute weight evenly among bags </b> <br/>
The idea of distribute weight evenly among bags is to avoid some bags are way heavier than the others. <br/>

---
<b><h3>Reasoning - Closed Domain QA System</h3></b>

Program has stored pair of questions and answers in QA bank. When user asks question, the program will do a mattern maching to find the most appropriate answer from QA bank as response.

