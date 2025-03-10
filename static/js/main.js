// Enable tooltips
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

// Function to handle the bookmark button
function toggleBookmark(testId) {
    // Implementation for bookmarking functionality
    console.log('Toggle bookmark for test: ' + testId);
}

// Initialize carousel
document.addEventListener('DOMContentLoaded', function() {
    const myCarousel = document.querySelector('#carouselExampleCaptions')
    if (myCarousel) {
        const carousel = new bootstrap.Carousel(myCarousel, {
            interval: 5000,
            wrap: true
        })
    }
});