/**
 * Template Name: Medilab
 * Updated: Sep 18 2023 with Bootstrap v5.3.2
 * Template URL: https://bootstrapmade.com/medilab-free-medical-bootstrap-theme/
 * Author: BootstrapMade.com
 * License: https://bootstrapmade.com/license/
 */

// Start upload preview image
// $(".gambar").attr("src", "/assets/img/img-upload.jpg");
$(".gambar").attr(
  "src",
  "https://github.com/manya706/Dermatological-Manifestation-SIH/blob/manya-changes-cut-branch-anuj/assets/img/img-upload.jpg?raw=true"
);
var $uploadCrop, tempFilename, rawImg, imageId;
function readFile(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $(".upload-demo").addClass("ready");
      $("#cropImagePop").modal("show");
      rawImg = e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    swal("Sorry - you're browser doesn't support the FileReader API");
  }
}

$uploadCrop = $("#upload-demo").croppie({
  viewport: {
    width: 500,
    height: 500,
  },
  enforceBoundary: false,
  enableExif: true,
});
$("#cropImagePop").on("shown.bs.modal", function () {
  // alert('Shown pop');
  $uploadCrop
    .croppie("bind", {
      url: rawImg,
    })
    .then(function () {
      console.log("jQuery bind complete");
    });
});

$(".item-img").on("change", function () {
  imageId = $(this).data("id");
  tempFilename = $(this).val();
  $("#cancelCropBtn").data("id", imageId);
  readFile(this);
});
$("#cropImageBtn").on("click", function (ev) {
  $uploadCrop
    .croppie("result", {
      type: "base64",
      format: "jpeg",
      size: { width: 500, height: 500 },
    })
    .then(function (resp) {
      $("#item-img-output").attr("src", resp);
      $("#cropImagePop").modal("hide");
    });
});
// End upload preview image

// Handle form submission when the user clicks the "Submit" button
$("#imageSelectionForm").on("submit", function (e) {
  // console.log("anujjjjjjjjjjjjjjjjj");
  // alert("2");
  e.preventDefault();

  // Create an array to hold image1 and image2
  var imagesArray = [];

  // Add image1 to the array
  imagesArray.push($(".item-img")[0].files[0]); // Uploaded image

  // Fetch the selected image file based on its filename
  var selectedImage = $("input[name='selectedImage']:checked").val();
  fetch("assets/img/WEBSITE_SAMPLES/" + selectedImage)
    .then((response) => response.blob())
    .then((blob) => {
      // Create a new File object from the blob for image2
      var selectedImageFile = new File([blob], selectedImage);

      // Add image2 to the array
      imagesArray.push(selectedImageFile);

      // Create a FormData object to store the images array and pincode
      var formData = new FormData();

      // Append the images array to the FormData
      formData.append("files", ...imagesArray);

      // Add the pincode separately to the FormData
      var pincode = $("#pincode").val();
      formData.append("pincode", pincode);

      // Send the FormData object to the server via a POST request
      $.ajax({
        url: "http://localhost:8000/form-predict/", // Replace with your FastAPI endpoint URL
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
          // Handle the response from the server
          // Display the output in the "output" <p> element
          $(".output").html(
            "Label: " +
              response.prediction.label +
              "<br>" +
              "Confidence: " +
              response.prediction.confidence +
              "<br>" +
              "Execution Time: " +
              response.exectime
          );
        },
        error: function (error) {
          // Handle any errors
          console.error(error);
        },
      });
    });

  // },
  // });
});

// ... Remaining JavaScript code ...

const img = document.querySelector(".row");
const tiltAmount = 10;

img.addEventListener("mousemove", (e) => {
  const { clientX, clientY } = e;
  const { left, top, width, height } = img.getBoundingClientRect();
  
  const xOffset = (clientX - left - width / 2) / (width / 2);
  const yOffset = (clientY - top - height / 2) / (height / 2);
  
  const xPos = xOffset * tiltAmount;
  const yPos = -yOffset * tiltAmount;
  
  img.style.transition = "transform 0.1s"; // Add a transition
  
  img.style.transform = `perspective(800px) rotateX(${yPos}deg) rotateY(${xPos}deg)`;
});

img.addEventListener("mouseleave", () => {
  img.style.transition = "transform 0.5s ease"; // Add a transition
  img.style.transform = "perspective(800px) rotateX(0deg) rotateY(0deg)";
});

