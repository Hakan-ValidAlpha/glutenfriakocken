// Sortering bara på katalogsidan (recept/). Ingredienstabeller på korten
// ska inte gå att sortera om av misstag med ett tryck på rubrikraden.
document$.subscribe(function () {
  if (!/\/recept\/(index\.html)?$/.test(location.pathname)) return
  var tables = document.querySelectorAll("article table:not([class])")
  tables.forEach(function (table) {
    new Tablesort(table)
  })
})
