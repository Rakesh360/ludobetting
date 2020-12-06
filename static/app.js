

    
function preview_image() 
{
 var total_file=document.getElementById("upload_file").files.length;
 console.log(total_file)
 for(var i=0;i<total_file;i++)
 {
  $('#image_preview').append("<img class='img-fluid img-responsive' style='height:100px ;width:100px' src='"+URL.createObjectURL(event.target.files[i])+"'>");
 }
}
