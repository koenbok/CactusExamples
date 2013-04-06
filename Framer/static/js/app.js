view = new View({x:100, y:100, width:300, height:100})

view.style = {
	backgroundColor: "rgba(0,100,100,.5)",
	padding: "20px"
}

view.html = "Hello world."

view.on("click", function() {
	view.scale = 0.5
	view.animateStop()
	view.animate({
		properties: {scale:1},
		curve: "spring(100,7,500)"
	})
	
})