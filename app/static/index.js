window.onload = () => {
	$('#sendbutton').click(() => {
		imagebox2 = $('#imagebox2')
		imagebox3 = $('#imagebox3')
		imagebox4 = $('#imagebox4')
        action = $('#action')[0]
		input = $('#imageinput')[0]
		var actionSelect = document.getElementById("action");
        var selectedAction = actionSelect.options[actionSelect.selectedIndex].text;

		if(input.files && input.files[0])
		{
			let formData = new FormData();
			formData.append('image' , input.files[0]);
			formData.append('image' , input.files[1]);
			console.log("action is " , selectedAction);

			formData.append('action' , selectedAction)


			$.ajax({
				url: "http://localhost:5000/maskImage",
				type:"POST",
				data: formData,
				cache: false,
				processData:false,
				contentType:false,
				error: function(data){
					console.log("upload error" , data);
					console.log(data.getAllResponseHeaders());
				},
				success: function(data){
//					alert("hello"); // if it's failing on actual server check your server FIREWALL + SET UP CORS
					bytestring = data['status']
					image = bytestring.split('\'')[1]
					bytestring = data['status1']
					image1 = bytestring.split('\'')[1]
					bytestring = data['status2']
					image2 = bytestring.split('\'')[1]

					imagebox2.attr('src' , 'data:image/jpeg;base64,'+image)
					imagebox3.attr('src' , 'data:image/jpeg;base64,'+image1)
					imagebox4.attr('src' , 'data:image/jpeg;base64,'+image2)
				}
			});
		}
	});
};

function readUrl(input){
	imagebox = $('#imagebox')
	imagebox1 = $('#imagebox1')
	console.log("evoked readUrl")
	if(input.files && input.files[0]){
		let reader = new FileReader();
		let reader1 = new FileReader();
		reader.onload = function(e){
			// console.log(e)
			imagebox.attr('src',e.target.result);
			imagebox.height(300);
			imagebox.width(300);
			console.log("displating image 1")
		}
		reader1.onload = function(e){
			// console.log(e)
			imagebox1.attr('src',e.target.result);
			imagebox1.height(300);
			imagebox1.width(300);
			console.log("disp img 2")
		}
		reader.readAsDataURL(input.files[0]);
		reader1.readAsDataURL(input.files[1]);
	}
}