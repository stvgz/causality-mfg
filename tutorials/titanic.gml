graph [
  directed 1
  node [
    id 0
    label "Survived"
  ]
  node [
    id 1
    label "Age"
  ]
  node [
    id 2
    label "Pclass"
  ]
  node [
    id 3
    label "Sex"
  ]
  node [
    id 4
    label "SibSp"
  ]
  node [
    id 5
    label "Parch"
  ]
  node [
    id 6
    label "Embarked"
  ]
  edge [
    source 1
    target 2
  ]
  edge [
    source 2
    target 0
  ]
  edge [
    source 3
    target 0
  ]
  edge [
    source 4
    target 5
  ]
  edge [
    source 5
    target 3
  ]
  edge [
    source 6
    target 2
  ]
]
