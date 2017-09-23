$(document).ready(function() {
$("#btn").click(function(e){
	var jsonData = {};
	var formData = $("#myform").serializeArray();
    
   
    $.each(formData, function() {
        if (jsonData[this.name]) {
           if (!jsonData[this.name].push) {
               jsonData[this.name] = [jsonData[this.name]];
           }
           jsonData[this.name].push(this.value || '');
       } else {
           jsonData[this.name] = this.value || '';
       }   
   });
   console.log(jsonData);
   /*$.ajax(
	{
		url : "test.php",
		type: "POST",
		data : jsonData,
		dataType: 'json',

        success:function(json) {
        	alert('Success!');
        }	

		
	});*/
    e.preventDefault();	
	});
});
function load() {
	console.log("Page load finished");
}

function addItinerary() {
	var myItinerary = document.getElementById('wrapper');
	//Prompt the user to type in start
	
	/*$(myItinerary).append(createElement('label', {
						    for: 'start',
						    textContent: 'Start Location:'
							}));
	$(myItinerary).append(createElement('input', {
									    type: 'text',
									    id: 'start',
									    name: 'start'
										}));
	$(myItinerary).append('<br>');
	*/
	
	//Prompt the user to type in start
	$(myItinerary).append(createElement('label', {
						    for: 'dest',
						    textContent: 'Destination:'
							}));
	$(myItinerary).append(createElement('input', {
									    type: 'text',
									    id: 'dest',
									    name: 'dest'
										}));
	$(myItinerary).append('<br>');

	//Prompt the user to type in duration
	$(myItinerary).append(createElement('label', {
						    for: 'duration',
						    textContent: 'Duration:'
							}));
	$(myItinerary).append(createElement('input', {
									    type: 'text',
									    id: 'duration',
									    name: 'duration'
										}));
	$(myItinerary).append('<br>');
	//Prompt the user to select a month
	$(myItinerary).append(createElement('label', {
						    for: 'month',
						    textContent: 'Travel Time:'
							}));
	$(myItinerary).append(createElement('input', {
							type:'month',
							id: 'month',
							name: 'month'
							}));
	$(myItinerary).append('<br>');
	//Prompt the user to select a budget descriptor
	$(myItinerary).append(createElement('label', {
						    for: 'budget',
						    textContent: 'Budget:'
							}));
	$(myItinerary).append(createElement('input', {
							type:'radio',
							id: 'budget',
							value: '0', 
							}));
	$(myItinerary).append('$');
	$(myItinerary).append(createElement('input', {
							type:'radio',
							id: 'budget',
							value: '1',
							}));
	$(myItinerary).append('$$');
	$(myItinerary).append(createElement('input', {
							type:'radio',
							id: 'budget',
							value: '2',
							}));
	$(myItinerary).append('$$$');
	$(myItinerary).append('<br>');
	$(myItinerary).append('<hr>');
	//$(myItinerary).append('</fieldset>');

	
}

function createElement (tagName, attrs) {
    var element = document.createElement(tagName);
    
    for (var attr in attrs) {
        if (!attrs.hasOwnProperty(attr)) continue;
        
        switch (attr) {
            case 'textContent':
            case 'innerHTML':
                element[attr] = attrs[attr];
                break;
                
            default:
                element.setAttribute(attr, attrs[attr]);
                break;
        }
    }
    
    //if (appendTo) appendTo.appendChild(element);
    return element;
}

//Collect html data and convert to JSON
/*function form_to_json(selector) {
	var ary = $(selector).serializeArray();
	var obj={};
	for (var a = 0; a < ary.length; ++a) {
		obj
	}
}*/
