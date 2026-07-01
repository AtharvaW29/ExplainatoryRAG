CREATE

(ml:Skill {
name:"Machine Learning"
}),

(calc:Concept {
name:"Calculus"
}),

(derivative:Concept {
name:"Derivative"
}),

(chain:Concept {
name:"Chain Rule"
}),

(backprop:Concept {
name:"Backpropagation"
}),

(neural:Concept {
name:"Neural Network"
}),

(m1:Misconception{
title:"Gradient flows unchanged through all layers"
}),

(book:LearningResource{
id:"book1",
title:"Deep Learning",
type:"Book"
});

MATCH (ml:Skill{name:"Machine Learning"}),
      (calc:Concept{name:"Calculus"}),
      (derivative:Concept{name:"Derivative"}),
      (chain:Concept{name:"Chain Rule"}),
      (backprop:Concept{name:"Backpropagation"}),
      (neural:Concept{name:"Neural Network"}),
      (m1:Misconception{title:"Gradient flows unchanged through all layers"}),
      (book:LearningResource{id:"book1"})

CREATE

(ml)-[:CONTAINS]->(backprop),

(calc)-[:PREREQUISITE_OF]->(derivative),

(derivative)-[:PREREQUISITE_OF]->(chain),

(chain)-[:PREREQUISITE_OF]->(backprop),

(backprop)-[:PREREQUISITE_OF]->(neural),

(book)-[:EXPLAINS]->(backprop),

(m1)-[:CAUSES_CONFUSION_WITH]->(backprop);
