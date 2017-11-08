function sortPlayerTable(n){
	var table = document.getElementById("table");
	var switching = true;
	var switch_count = 0;
	var dir = "asc";
	while(switching){

		switching = false;
		var rows = table.getElementsByTagName("tr");

		for (var current_row_index = 1; current_row_index < (rows.length - 1); current_row_index ++){
			var shouldSwitch = false;
			var current_row = rows[current_row_index].getElementsByTagName('td')[n];
			var next_row = rows[current_row_index + 1].getElementsByTagName('td')[n];

			if (dir == "asc"){
				if (current_row.innerHTML.toLowerCase() > next_row.innerHTML.toLowerCase()){
					shouldSwitch = true;
					break;
				}
			}
			else if (dir == "desc"){
				if (current_row.innerHTML.toLowerCase() < next_row.innerHTML.toLowerCase()){
					shouldSwitch = true;
					break;
				}
			}
		}
    display_color = 0;
		if (shouldSwitch) {
			rows[current_row_index].parentNode.insertBefore(rows[current_row_index + 1],rows[current_row_index]);
			switching = true;
			switch_count ++;
		}
		else{
			if (switch_count == 0 && dir == "asc"){
				dir = "desc";
				switching = true;
			}
		}
	}
}

function PlayerFilterFunction(team_index, value_index ){
	var team_filter = document.getElementById("team_dropdown").value.toUpperCase();
	var value_filter = document.getElementById("value_dropdown").value.toUpperCase();
	var table = document.getElementById("table");
  	var rows = table.getElementsByTagName("tr");

  	for (var i = 0; i < (rows.length); i++){
  		rows[i].style.display = "";
  	}
    var display_color = 0;
  	for (var i = 1; i < (rows.length); i++){
  		//alert(search_filter+team_filter+position_filter);
  		var cur_row_team = rows[i].getElementsByTagName("td")[team_index];
  		var cur_row_val  = rows[i].getElementsByTagName("td")[value_index];


  		//team filter
  		if (cur_row_team){
  			var team_bool = (cur_row_team.innerHTML.toUpperCase().indexOf(team_filter) > -1);
  		}
  		var team_all = (team_filter == "ALL");

  		//value filter
  		if (cur_row_val){
  			var val_bool = (cur_row_val.innerHTML.toUpperCase().indexOf(value_filter) > -1);
  		}
  		var val_all = (value_filter == "ALL");


  		if ((team_bool||team_all)&&(val_bool||val_all)) {
  			rows[i].style.display = "";
        // setColors(display_color, rows[i]);

  		}
  		else{
  			rows[i].style.display = "none";
  		}


  	}
}