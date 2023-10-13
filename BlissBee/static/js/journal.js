/* Submit on Enter */
$("#addNewItemInput").on("keydown", (e) => {
  if (e.keyCode === 13) {
    $("#addNewItemBtn").click()
    $("#addNewItemInput").val("")
  }
})

$("#titleInput").on("keydown", (e) => {
  if (e.keyCode == 13) {
    $("#titleInput").blur();
  }
})

/* Add a new item */
$("#addNewItemBtn").on("click", (e) => {
  if ($("#addNewItemInput").val() == "") {
    gsap.to("#addNewItemInput", .1, {x: -4})
    gsap.to("#addNewItemInput", .1, {delay: .1, x: 4})
    gsap.to("#addNewItemInput", .1, {delay: .2, x: -4})
    gsap.to("#addNewItemInput", .1, {delay: .3, x: 4})
    gsap.to("#addNewItemInput", .1, {delay: .4, x: 0})
  } else {
    const newItemInput = $("#addNewItemInput").val()
  
  $(".item").append(
    `<div class="itemInner">
      <i class="far fa-hand-point-right"></i>
      <p>${newItemInput}</p>
      <button class="removeItemBtn">
       <i class="fas fa-trash-alt"></i>
      </button>
     </div>`)
  
  $("#addNewItemInput").val("")
  
  const newItem = e.target

  gsap.to(".itemsWrapper, .item", .3, {paddingBottom: 30, ease: Back.easeOut})
  gsap.to(".itemsWrapper, .item", .3, {delay: .15, paddingBottom: 8, y: 0, ease: Back.easeOut})
  }
})

/* Completed item line through */
$(".item").on("click", "i.fa-hand-point-right", (e) => {
  const handPoint = e.target
  const completedItem = e.target.parentElement
  const text = completedItem.getElementsByTagName('p')
  
  $(text).css({"text-decoration": "line-through"})
  gsap.to(handPoint, .3, {rotate: -30, transformOrigin: "center", ease: Back.easeOut})
  gsap.to(handPoint, .3, {delay: .15, rotate: 0, transformOrigin: "center", ease: Back.easeOut})
})

/* Remove item */
$(".item").on("click", "button.removeItemBtn", (e) => {
    const removeItem = e.target
    const itemInner = removeItem.parentElement    
    $(itemInner).remove()
  
  gsap.to(".itemsWrapper, .item", 0, {paddingBottom: 52})
  gsap.to(".itemsWrapper, .item", .3, {paddingBottom: 8, ease: Back.easeOut})
})

/* Edit list title animation */
gsap.set(".fa-pencil-alt", {opacity: 0, rotate: -180, transformOrigin: "center"})
gsap.set("#titleInput, #addNewItemInput", {border: "1px solid transparent", boxShadow: "0 0 0 rgba(211, 220, 248, .3)"})

$("#titleInput").on("mouseenter", () => {
    gsap.to(".fa-pencil-alt", .3, {rotate: 0, opacity: 1, transformOrigin: "center", ease: Back.easeOut})
})

$("#titleInput").on("mouseleave", () => {
  if ($("#titleInput").is(":focus")) {
    gsap.to(".fa-pencil-alt", .3, {rotate: 0, opacity: 1, transformOrigin: "center", ease: Back.easeOut})
  } else if (!($("#titleInput").is(":focus"))) {
    gsap.to(".fa-pencil-alt", .3, {rotate: -180, opacity: 0, transformOrigin: "center", ease: Back.easeOut})
  }
})

$("#titleInput").on("focus", () => {
  gsap.to(".fa-pencil-alt", .3, {rotate: 0, opacity: 1, transformOrigin: "center", ease: Back.easeOut})
  gsap.to("#titleInput", .3, {border: "1px solid #e7ecfb", boxShadow: "0 0 12px rgba(211, 220, 248, .3)"})
})

$("#titleInput").on("focusout", () => {
  gsap.to(".fa-pencil-alt", .3, {rotate: -180, opacity: 0, transformOrigin: "center", ease: Back.easeOut})
  gsap.to("#titleInput", .3, {border: "1px solid transparent", boxShadow: "0 0 12px rgba(211, 220, 248, 0)"})
})

/* Trash fade on item hover */
$(".item").on("mouseenter", ".itemInner", (e) => {
  const trashBtn = $(e.target.querySelector(".removeItemBtn"))
  gsap.to(trashBtn, .3, {opacity: 1})
})

$(".itemInner").on("mouseenter", ".removeItemBtn", (e) => {
  const trashBtn = e.target
  gsap.to(trashBtn, .3, {opacity: 1})
})

$(".innerItem").on("mouseleave", ".removeItemBtn", (e) => {
  gsap.to(trashBtn, .3, {opacity: 0})
})

$(".item").on("mouseleave", ".itemInner", (e) => {
  const trashBtn = $(e.target.querySelector(".removeItemBtn"))
  gsap.to(trashBtn, .3, {opacity: 0})
})

$(".itemInner").on("mouseleave", ".removeItemBtn", (e) => {
  const trashBtn = e.target
  gsap.to(trashBtn, .3, {opacity: 0})
})

/* Add a new item animation */
$("#addNewItemInput").on("focus", () => {
  gsap.to("#addNewItemInput", .3, {border: "1px solid #e7ecfb", boxShadow: "0 0 12px rgba(211, 220, 248, .3)"})
})

$("#addNewItemInput").on("focusout", () => {
  gsap.to("#addNewItemInput", .3, {border: "1px solid transparent", boxShadow: "0 0 12px rgba(211, 220, 248, 0)"})
})

$("#addNewItemBtn").on("mouseenter", () => {
  gsap.to(".fa-plus", .3, {rotate: 90, ease: Back.easeOut})
})

$("#addNewItemBtn").on("mouseleave", () => {
  gsap.to(".fa-plus", .3, {rotate: 0, ease: Back.easeOut})
})