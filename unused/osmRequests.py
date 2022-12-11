

q1 = """
    relation[network="Verkehrsverbund Berlin-Brandenburg"]
      [operator = "regiobus Potsdam Mittelmark GmbH"]
      [public_transport=stop_area]({{bbox}});

    out center;"""
    
q2 = """
area[file_path="Brandenburg an der Havel"]->.searchArea;

nwr[public_transport=station](area.searchArea);
out center;

nwr._->.res;

nwr[amenity=bar](around.res:1000);
        
out center;"""

q3_working = """
area[file_path="Berlin"]->.searchArea;

nwr[public_transport=station](area.searchArea);
nwr._->.res; // needs to be on two lines
out center;

nwr[amenity=bar](around.res:100);
        
out center;

{{style:
node { 
  color:black; 
  fill-color:red;
}

node[public_transport=station] { 
  color:green;
  fill-color:none;
  fill-opacity:20%
}
}}
"""

q4 = """
area[file_path="Brandenburg"]->.searchArea;

nwr[public_transport=station](area.searchArea);
nwr._->.res; // needs to be on two lines
out center;

nwr[amenity=bar](around.res:100);        
out center;

relation[boundary=administrative][admin_level=4]({{bbox}}); // how to make dis work
out center;

{{style:
node[amenity=bar] { 
  color:black; 
  fill-color:red;
  text:file_path;
}

node[public_transport=station] { 
  color:green;
  fill-color:none;
  fill-opacity:20%
}
}}
"""

q5 = """
area[file_path="Berlin"]->.searchArea;

//nwr[public_transport=station](area.searchArea);
nwr(id:3870914569);
nwr._->.res; // needs to be on two lines
out center;

nwr[amenity=bar](around.res:1000);        
out center;

out center;

{{style:
node[amenity=bar] { 
  color:black; 
  fill-color:red;
  /*text:file_path;*/
}

node[public_transport=station] { 
  color:green;
  fill-color:none;
  fill-opacity:20%
}
}}
"""