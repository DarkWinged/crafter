# crafter

### Description

This is a python app that provides an api for users to access a crafting database. This database holds tables containng items, recipies, ingredients, and products.

#### Tables

| name       | contents                             | key           | role                                                             |
| ---------- | ------------------------------------ | ------------- | ---------------------------------------------------------------- |
| item       | item names, descriptions, etc        | item id       | table storing describing items                                   |
| recipe     | recipe names, descritpions, etc      | recipe id     | table storing data describing recipes                            |
| ingredient | recipe id, item id, units per minute | ingredient id | bridge table desribing what ingridents are consumbed by a recipe |
| product    | recipe id, item id, units per minute | product id    | bridge table desribing what products are produced by a recipe    |

#### Endpoints

- GET /items # returns all items
- GET /items/{item_id} # returns item with id item_id
- POST /items # creates new items from json body
- PUT /items/{item_id} # updates or creates item at item_id
- DELETE /items/{item_id} # deletes item at item_id
- GET /recipes # returns all recipes
- GET /recipes/{recipe_id} # returns recipe with id recipe_id
- POST /recipes # creates new recipes from json body
- PUT /recipes/{recipe_id} # updates or creates recipe at recipe_id
- DELETE /recipes/{recipe_id} # deletes recipe at recipe_id
- GET /ingredients # returns all ingredients
- GET /ingredients/{ingredient_id} # returns ingredient with id ingredient_id
- POST /ingredients # creates new ingredients from json body
- PUT /ingredients/{ingredient_id} # updates or creates ingredient at ingredient_id
- DELETE /ingredients/{ingredient_id} # deletes ingredient at ingredient_id
- GET /products # returns all products
- GET /products/{product_id} # returns product with id product_id
- POST /products # creates new products from json body
- PUT /products/{product_id} # updates or creates product at product_id
- DELETE /products/{product_id} # deletes product at product_id
- POST /recipe # creates new item, recipe, ingredients, and products from json body
- POST /craft/{recipe_id}/{scale} # returns the ingredients consumed and products produced by crafting recipe_id at scale
- PUT /craft # returns the ingredients consumed and products produced by crafting recipe_id at scale
- PUT /craft/tree # returns the ingredients consumed and products produced by crafting recipe_id at scale and all precursor recipes up to depth or until all root recipes are reached
