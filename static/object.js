var  text_box = {}
var axis = []
var shape={c:'draw_circle', o:'draw_oval', s:'draw_square', r:"draw_rectangle", d:"draw_diamond"}


function wfAddModal(){
   var wfModal = document.getElementById("workFlow")
   var close = document.getElementsByClassName('popupCloseButton')[0]
   wfModal.style.display = "block"
   close.onclick = function(){
        wfModal.style.display = "none"
   }

}

function wfRetModal(){
   var retModal = document.getElementById("retWorkFlow")
   var closeRet = document.getElementsByClassName('popupCloseButton')[0]
   var close = document.getElementById('close')
   retModal.style.display = "block"
   close.onclick = function(){
        retModal.style.display = "none"
   }
}

function addShapesModal(){
   var addShape = document.getElementById("AddShape")
   var closeAddShape = document.getElementsByClassName("popupCloseButton")[0]
   addShape.style.display  = "block"
   closeAddShape.onclick = function(){
        addShape.style.display = "none"
   }
}

function draw_shapes(id, heading, i, desc, y, num, count, lastAxis){
    axis.push(y)
    sh = i.toString()
    sh_1 = sh.slice(14,15)
    heading = heading.toLowerCase();
    newHeading = heading.replace(/&lt;/g,"<")
    newHeading = newHeading.replace(/&gt;/g,">")
    newDesc = desc.replace(/&lt;/g,"<")
    newDesc = newDesc.replace(/&gt;/g,">")
    newDesc_1 = newDesc.replace(/<br>/g, '\n')
        text_box[y] = [newDesc_1, newHeading, id, sh_1]
    var draw = i;

    shape_desc = draw(newHeading, y, count, num)
    console.log('LAST AXIS', lastAxis)
    scrollToBtm(lastAxis);
}


function draw_square(heading, y, count, num) {
   var c1 = document.getElementById('canvas');
   var cl_draw = c1.getContext("2d");
   cl_draw.beginPath();
   cl_draw.rect(500, y, 150, 150);
   cl_draw.stroke();
   cl_draw.font = "24px Arial";
   cl_draw.fillStyle = "#800000";
    var width = cl_draw.measureText(heading).width;
   console.log('width', heading.length)
   var height = cl_draw.measureText("w").width;
   len = heading.length
   console.log('len',len)
   if (len <= 10){
    cl_draw.fillText(heading, 575 - (width/2),y + (height/2) + 75)
    }
 else if(len<=20){
    console.log('inside')
    headingPart_1 = heading.slice(0, 8) + '-'
    headingPart_2 = heading.slice(8,)
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 62)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 90)
}
    else if(len<=40) {
       cl_draw.font = "20px Arial";

        headingPart_1 = heading.slice(0, 15) + '-'
    headingPart_2 = heading.slice(15,30) + '-'
    headingPart_3 = heading.slice(30,)
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 50)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 75)
        cl_draw.fillText(headingPart_3, 575 - (width_2/2), y + (height/2) + 100)



    }
    else{
           cl_draw.font = "15px Arial";

    headingPart_1 = heading.slice(0, 18) + '-'
    headingPart_2 = heading.slice(18, 36) + '-'
    headingPart_3 = heading.slice(36, )
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    var width_3 = cl_draw.measureText(headingPart_3).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 50)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 75)
    cl_draw.fillText(headingPart_3, 575 - (width_3/2), y + (height/2) + 100)



    }
   if (num!=count){
        draw_arrow(y);
   }
}


function draw_circle(heading, y, count, num) {
   var c1 = document.getElementById('canvas');
   var cl_draw = c1.getContext("2d");

   cl_draw.beginPath();
   cl_draw.arc(575, y + 75, 75, 0, Math.PI*2);
   cl_draw.stroke();
   cl_draw.font = "24px Arial";
   cl_draw.fillStyle =  "#800000";
   var width = cl_draw.measureText(heading).width;
   console.log('width', heading.length)
   var height = cl_draw.measureText("w").width;
   len = heading.length
   console.log('len',len)
   if (len <= 10){
    cl_draw.fillText(heading, 575 - (width/2),y + (height/2) + 75)
    }
   else if(len<=20){
    console.log('inside')
    headingPart_1 = heading.slice(0, 8) + '-'
    headingPart_2 = heading.slice(8,)
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 62)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 90)
}
    else if(len<=40) {
    console.log("hello inside 2nd loop")
       cl_draw.font = "18px Arial";

    headingPart_1 = heading.slice(0, 10) + '-'
    headingPart_2 = heading.slice(10, 25) + '-'
    headingPart_3 = heading.slice(25, );
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    var width_3 = cl_draw.measureText(headingPart_3).width;
    console.log('HEADING PART***********0', headingPart_1, headingPart_2, headingPart_3)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 34)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 62)
    cl_draw.fillText(headingPart_3, 575 - (width_3/2), y + (height/2) + 90)
    }
    else{
        console.log("hello inside 3rd loop")

    cl_draw.font = "15px Arial";

    headingPart_1 = heading.slice(0, 17) + '-'
    headingPart_2 = heading.slice(17, 35) + '-'
    headingPart_3 = heading.slice(35, )

    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    var width_3 = cl_draw.measureText(headingPart_3).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 50)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 75)
    cl_draw.fillText(headingPart_3, 575 - (width_3/2), y + (height/2) + 100)



    }
   if (num != count){
        draw_arrow(y);
   }
}

function draw_rectangle(heading, y, count, num) {
   var c1 = document.getElementById('canvas');
   var cl_draw = c1.getContext("2d");
   cl_draw.beginPath();
   cl_draw.rect(465, y, 225, 150);
   cl_draw.stroke();
   cl_draw.font = "24px Arial";
   cl_draw.fillStyle =  "#800000";
   var width = cl_draw.measureText(heading).width;
   console.log('width', heading.length)
   var height = cl_draw.measureText("w").width;
   len = heading.length
   console.log('len',len)
   if (len <= 10){
    cl_draw.fillText(heading, 575 - (width/2),y + (height/2) + 75)
    }
   else if(len<=20){
    console.log('inside')
    headingPart_1 = heading.slice(0, 8) + '-'
    headingPart_2 = heading.slice(8,)
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 62)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 90)
}
    else if(len<=40) {
       cl_draw.font = "20px Arial";

        headingPart_1 = heading.slice(0, 19) + '-'
    headingPart_2 = heading.slice(19,)
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 62)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 90)


    }
    else{
           cl_draw.font = "15px Arial";

    headingPart_1 = heading.slice(0, 18) + '-'
    headingPart_2 = heading.slice(18, 36) + '-'
    headingPart_3 = heading.slice(36, )
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    var width_3 = cl_draw.measureText(headingPart_3).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 50)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 75)
    cl_draw.fillText(headingPart_3, 575 - (width_3/2), y + (height/2) + 100)



    }
   if (num != count){
        draw_arrow(y);
   }
}

function draw_oval(heading, y, count, num){
    var c1 = document.getElementById('canvas');
    var cl_draw = c1.getContext("2d");
    cl_draw.beginPath();
    cl_draw.ellipse(575, y + 75, 120, 75, 0, 0, Math.PI*2);
    cl_draw.stroke();
      cl_draw.font = "24px Arial";
   cl_draw.fillStyle =  "#800000";
   var width = cl_draw.measureText(heading).width;
   console.log('width', heading.length)
   var height = cl_draw.measureText("w").width;
   len = heading.length
   console.log('len',len)
   if (len <= 10){
    cl_draw.fillText(heading, 575 - (width/2),y + (height/2) + 75)
    }
   else if(len<=20){
    console.log('inside')
    headingPart_1 = heading.slice(0, 8) + '-'
    headingPart_2 = heading.slice(8,)
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 62)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 90)
}
    else if(len<=40){

           cl_draw.font = "15px Arial";

        headingPart_1 = heading.slice(0, 15) + '-'
    headingPart_2 = heading.slice(15,30) + '-'
        headingPart_3 = heading.slice(30,)

    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
        var width_3 = cl_draw.measureText(headingPart_3).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 50)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 75)
        cl_draw.fillText(headingPart_3, 575 - (width_3/2), y + (height/2) + 100)


    }
    else{
           cl_draw.font = "15px Arial";

    headingPart_1 = heading.slice(0, 18) + '-'
    headingPart_2 = heading.slice(18, 36) + '-'
    headingPart_3 = heading.slice(36, )
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    var width_3 = cl_draw.measureText(headingPart_3).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 50)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 75)
    cl_draw.fillText(headingPart_3, 575 - (width_3/2), y + (height/2) + 100)



    }
 if (num != count){
        draw_arrow(y);
    }
}

function draw_diamond(heading, y, count, num){
    var c1 = document.getElementById('canvas');
    var cl_draw = c1.getContext("2d");

    cl_draw.beginPath();
    cl_draw.moveTo(572,y);
    cl_draw.lineTo(672,y + 74.5);
    cl_draw.lineTo(572,y + 149);
    cl_draw.lineTo(472,y + 74.5);
    cl_draw.closePath();
    cl_draw.stroke();
    cl_draw.font = "24px Arial";
    cl_draw.fillStyle =  "#800000";
    var width = cl_draw.measureText(heading).width;
    console.log('width', heading.length)
    var height = cl_draw.measureText("w").width;
    len = heading.length
    console.log('len',len)
    if (len <= 10){
     cl_draw.fillText(heading, 575 - (width/2),y + (height/2) + 75)
    }
 if (len <= 10){
    cl_draw.fillText(heading, 575 - (width/2),y + (height/2) + 75)
    }
   else if(len<=20){
    console.log('inside')
    headingPart_1 = heading.slice(0, 8) + '-'
    headingPart_2 = heading.slice(8,)
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 62)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 90)
}
    else if(len<=40) {
       cl_draw.font = "20px Arial";

        headingPart_1 = heading.slice(0, 19) + '-'
    headingPart_2 = heading.slice(19,)
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 62)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 90)


    }
    else{
           cl_draw.font = "15px Arial";

    headingPart_1 = heading.slice(0, 18) + '-'
    headingPart_2 = heading.slice(18, 36) + '-'
    headingPart_3 = heading.slice(36, )
    var width_1 = cl_draw.measureText(headingPart_1).width;
    var width_2 = cl_draw.measureText(headingPart_2).width;
    var width_3 = cl_draw.measureText(headingPart_3).width;
    console.log(headingPart_1, headingPart_2)
    cl_draw.fillText(headingPart_1, 575 - (width_1/2), y + (height/2) + 50)
    cl_draw.fillText(headingPart_2, 575 - (width_2/2), y + (height/2) + 75)
    cl_draw.fillText(headingPart_3, 575 - (width_3/2), y + (height/2) + 100)



    }

    if (num != count){
        console.log("inside diamond for creating arrow")
        draw_arrow(y);
    }
}


function draw_arrow(y){
  var c1 = document.getElementById('canvas');
  var c1_context = c1.getContext('2d');
  c1_context.beginPath();
  c1_context.moveTo(572,y + 150);
  c1_context.lineTo(572,y + 250);
  c1_context.stroke();
   arrowHead(y);

}

function arrowHead(y,){
  var c1 = document.getElementById('canvas');
  var ctx = c1.getContext('2d');

  ctx.moveTo(566,y + 245);
  ctx.lineTo(578,y + 245);
  ctx.lineTo(572,y + 250);
  ctx.lineTo(566,y + 245);
  ctx.fillStyle = "black"
  ctx.stroke();
  ctx.fill();
//  scrollToBtm();
}

function point_it(event) {
        pos_x = event.offsetX ? (event.offsetX) : event.pageX - document.getElementById("pointer_div").offsetLeft;
        pos_y = event.offsetY ? (event.offsetY) : event.pageY - document.getElementById("pointer_div").offsetTop;
        console.log(pos_x)
        console.log(pos_y)


        desc_prompt(pos_x, pos_y);
    }

    function desc_prompt(pos_x, pos_y){
    var closest = axis.reduce(function(prev, curr) {
        return (Math.abs(curr - pos_y) < Math.abs(prev - pos_y) ? curr : prev);
});
    console.log(closest);
    if  (pos_x >= 500 && pos_x <= 650) {
        var modal2 = document.getElementById("DescPopup");
//        var close = document.getElementById('close')
        var span = document.getElementsByClassName("popupCloseButton")[0];
        document.getElementById("shapeId").innerHTML = "Shape Id:" + "   " + "   " +text_box[closest][2]
        document.getElementById("delId").value = text_box[closest][2]
        document.getElementById("heading").innerHTML ="Heading:" + "   " + "   " + text_box[closest][1]
        document.getElementById("description").innerHTML = text_box[closest][0];
//        document.getElementById("modId").value = text_box[closest][2];
        document.getElementById("originalId").value = text_box[closest][2];
//        document.getElementById("modHeading").value = text_box[closest][1];
        document.getElementById("input").value = text_box[closest][2]
        originalId = text_box[closest][2]
        type = text_box[closest][3]

        document.getElementById("shape").value = shape[type];
//        document.getElementById("modDesc").value = text_box[closest][0];
        document.getElementById('sID').value = text_box[closest][2]
        document.getElementById('sHeading').value = text_box[closest][1]
        document.getElementById('subject').innerHTML = text_box[closest][0]
        document.getElementById('formHeading').innerHTML = 'Modify Shape Details'
        modal2.style.display = "block";

        span.onclick = function() {
        modal2.style.display = "none";
    }

}
}

function modModal(){
var modal = document.getElementById('AddShape')
var button = document.getElementById('submit_form')
var descModal = document.getElementById('DescPopup')
var close = document.getElementById('closeDesc')
//var close = document.getElementsByClassName('popupCloseButton')[0]
descModal.style.display = 'none'
button.value = 'Modify_Form'
button.innerHTML = "Modify"
modal.style.display = 'block'

close.onclick = function (){
    modal.style.display = 'none'
}
}


function errorShapeId(error){

    var errorModal = document.getElementById("ErrorPopup")
    var span = document.getElementsByClassName("popupCloseButton")[0];
    var close = document.getElementById('closeError')
    document.getElementById("errorMsg").innerHTML = error
    errorModal.style.display = "block";
    close.onclick = function(){
      errorModal.style.display = "none";
      }
      window.onclick = function(event) {
  if (event.target == errorModal) {
    errorModal.style.display = "none";
  }
}
}

function scrollToBtm(lastAxis){
    console.log('inside', lastAxis)
    window.scrollTo(0, lastAxis);

}