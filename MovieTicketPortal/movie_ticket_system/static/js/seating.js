document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    const seatContainer = document.getElementById('seatContainer');
    const selectedSeatsElement = document.getElementById('selectedSeats');
    const totalPriceElement = document.getElementById('totalPrice');
    const continueBtn = document.getElementById('continueBtn');
    const showtime = document.getElementById('showtime');
    
    // Extract data from data attributes
    const showtimeId = showtime.dataset.showtimeId;
    const ticketPrice = parseFloat(showtime.dataset.price);
    const rows = parseInt(showtime.dataset.rows);
    const seatsPerRow = parseInt(showtime.dataset.seatsPerRow);
    let bookedSeatsArray = showtime.dataset.bookedSeats ? showtime.dataset.bookedSeats.split(',') : [];
    
    // Variables to track selected seats
    let selectedSeats = [];
    
    // Create the theater layout
    function createTheaterLayout() {
        // Clear existing content
        seatContainer.innerHTML = '';
        
        // Create rows (A, B, C, etc.)
        for (let i = 0; i < rows; i++) {
            const rowLetter = String.fromCharCode(65 + i); // ASCII 'A' starts at 65
            
            const rowDiv = document.createElement('div');
            rowDiv.className = 'seat-row';
            
            // Add row label
            const rowLabel = document.createElement('div');
            rowLabel.className = 'row-label';
            rowLabel.textContent = rowLetter;
            rowDiv.appendChild(rowLabel);
            
            // Create seats in this row
            for (let j = 1; j <= seatsPerRow; j++) {
                const seat = document.createElement('div');
                seat.className = 'seat';
                seat.textContent = j;
                
                // Set seat data
                const seatId = `${rowLetter}${j}`;
                seat.dataset.id = seatId;
                
                // Check if this seat is already booked
                if (bookedSeatsArray.includes(seatId)) {
                    seat.classList.add('booked');
                } else {
                    // Add click event for available seats
                    seat.addEventListener('click', () => toggleSeat(seat, seatId));
                }
                
                rowDiv.appendChild(seat);
            }
            
            seatContainer.appendChild(rowDiv);
        }
    }
    
    // Toggle seat selection
    function toggleSeat(seatElement, seatId) {
        if (seatElement.classList.contains('booked')) {
            return; // Can't select booked seats
        }
        
        if (seatElement.classList.contains('selected')) {
            // Deselect the seat
            seatElement.classList.remove('selected');
            const index = selectedSeats.indexOf(seatId);
            if (index > -1) {
                selectedSeats.splice(index, 1);
            }
        } else {
            // Select the seat
            seatElement.classList.add('selected');
            selectedSeats.push(seatId);
        }
        
        // Update the UI
        updateSelectedSeatsInfo();
    }
    
    // Update selected seats information
    function updateSelectedSeatsInfo() {
        if (selectedSeats.length > 0) {
            selectedSeats.sort(); // Sort seats for better display
            selectedSeatsElement.textContent = selectedSeats.join(', ');
            const total = (selectedSeats.length * ticketPrice).toFixed(2);
            totalPriceElement.textContent = `$${total}`;
            continueBtn.classList.remove('disabled');
            continueBtn.href = `/showtime/${showtimeId}/book?seats=${selectedSeats.join(',')}`;
        } else {
            selectedSeatsElement.textContent = 'None';
            totalPriceElement.textContent = '$0.00';
            continueBtn.classList.add('disabled');
            continueBtn.href = '#';
        }
    }
    
    // Check for updates to booked seats periodically
    function checkForUpdates() {
        fetch(`/api/get-booked-seats/${showtimeId}`)
            .then(response => response.json())
            .then(data => {
                const newBookedSeats = data.booked_seats;
                
                // Check if any new seats have been booked
                if (JSON.stringify(bookedSeatsArray) !== JSON.stringify(newBookedSeats)) {
                    bookedSeatsArray = newBookedSeats;
                    
                    // Check if any of the currently selected seats have been booked
                    const newlyBooked = selectedSeats.filter(seat => bookedSeatsArray.includes(seat));
                    
                    if (newlyBooked.length > 0) {
                        // Remove newly booked seats from selection
                        selectedSeats = selectedSeats.filter(seat => !bookedSeatsArray.includes(seat));
                        
                        // Alert the user
                        alert(`Sorry, the following seats have just been booked: ${newlyBooked.join(', ')}. They have been removed from your selection.`);
                        
                        // Recreate the theater layout
                        createTheaterLayout();
                        
                        // Reselect the remaining selected seats
                        selectedSeats.forEach(seatId => {
                            const seatElement = document.querySelector(`.seat[data-id="${seatId}"]`);
                            if (seatElement) {
                                seatElement.classList.add('selected');
                            }
                        });
                        
                        // Update the UI
                        updateSelectedSeatsInfo();
                    } else {
                        // Just update the visual state of seats
                        bookedSeatsArray.forEach(seatId => {
                            const seatElement = document.querySelector(`.seat[data-id="${seatId}"]`);
                            if (seatElement) {
                                seatElement.classList.add('booked');
                                seatElement.classList.remove('selected');
                                
                                // Remove from selected if it was selected
                                const index = selectedSeats.indexOf(seatId);
                                if (index > -1) {
                                    selectedSeats.splice(index, 1);
                                    updateSelectedSeatsInfo();
                                }
                            }
                        });
                    }
                }
            })
            .catch(error => console.error('Error checking for seat updates:', error));
    }
    
    // Initialize
    createTheaterLayout();
    updateSelectedSeatsInfo();
    
    // Check for updates every 30 seconds
    setInterval(checkForUpdates, 30000);
});
