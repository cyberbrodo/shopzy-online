// CART STORAGE

let cart = JSON.parse(localStorage.getItem("cart")) || [];


// ADD TO CART

function addToCart(name, price){

    cart.push({name, price});

    localStorage.setItem("cart", JSON.stringify(cart));

    alert(name + " added to cart 🛒");
}


// SEARCH BOX OPEN / CLOSE

const searchWrapper = document.querySelector(".search-wrapper");

const searchBtn = document.querySelector("#searchBtn");

searchBtn.addEventListener("click", () => {

    searchWrapper.classList.toggle("active");

});


// PRODUCT SCROLL LEFT

function scrollLeft(){

    document.getElementById("latest").scrollBy({

        left: -300,

        behavior: "smooth"

    });

}


// PRODUCT SCROLL RIGHT

function scrollRight(){

    document.getElementById("latest").scrollBy({

        left: 300,

        behavior: "smooth"

    });

}


// NAVBAR SHADOW ON SCROLL

const navbar = document.querySelector(".custom-nav");

window.addEventListener("scroll", () => {

    if(window.scrollY > 50){

        navbar.style.boxShadow = "0 4px 20px rgba(0,0,0,0.25)";

    }

    else{

        navbar.style.boxShadow = "none";

    }

});


// PRODUCT HOVER EFFECT

const products = document.querySelectorAll(".product");

products.forEach((product) => {

    product.addEventListener("mouseenter", () => {

        product.style.transform = "translateY(-8px)";

        product.style.transition = "0.3s";

    });

    product.addEventListener("mouseleave", () => {

        product.style.transform = "translateY(0px)";

    });

});