new Vue({
    delimiters: ['{$', '$}'],
    el: '#app',
    data: {
      credentials: {},
      username: null,
      jwt: '',
      page_title: 'My Library Manager',
      activities: [],
      books: [],
      book: {},
      newBook: {},
      locations: [],
      location: {},
      newLocation: {},
      loans: [],
      loan: {},
      newLoan: {},
      loginVisible: false,
      navbarVisible: false,
      homeVisible: false,
      booksVisible: false,
      allBooksVisible: false,
      newBookVisible: false,
      updateBookVisible: false,
      deleteBookVisible: false,
      locationsVisible: false,
      allLocationsVisible: false,
      newLocationVisible: false,
      updateLocationVisible: false,
      deleteLocationVisible: false,
      loansVisible: false,
      allLoansVisible: false,
      newLoanVisible: false,
      returnLoanVisible: false,
    },
    http: {
      root: 'http://localhost:8000/',
      headers: {}
    },
    methods: {
        // JWT Auth
        async fetchJWT() {
          this.loading = true;
          this.$http.post('/auth-jwt/', this.credentials)
            .then((response) => {
              this.loading = true;
              // save token data from response
              localStorage.jwt = response.data['token']
              this.jwt = localStorage.jwt;
              // save user name
              localStorage.username = this.credentials['username'];
              this.username = localStorage.username;
              // load the rest
              this.getBooks();
              this.getLocations();
              this.getLoans();
              this.showHome();
            })
            .catch((err) => {
              this.loading = false;
              console.log(err);
            })
        },
        // Logout
        logout: function(){
          // delete username, credentials, token
          this.username = null;
          this.credentials = {};
          this.jwt = '';
          localStorage.setItem('jwt', null);

          // delete books, locations, loans
          this.books = [];
          this.locations = [];
          this.loans = [];

          // showLogin
          this.showLogin();
        },
        // UI Controllers
        showLogin: function(){
          this.loginVisible = true;
          this.homeVisible = false;
          this.navbarVisible = false;
          this.booksVisible = false;
          this.locationsVisible = false;
          this.loansVisible = false;
          this.allBooksVisible = false;
          this.newBookVisible = false;
          this.updateBookVisible = false;
          this.deleteBookVisible = false;
          this.allLocationsVisible = false;
          this.newLocationVisible = false;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = false;
          this.allLoansVisible = false;
          this.newLoanVisible = false;
          this.returnLoanVisible = false;
        },
        // Home
        showHome: function(){
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = true;
          this.booksVisible = false;
          this.allBooksVisible = false;
          this.newBookVisible = false;
          this.updateBookVisible = false;
          this.deleteBookVisible = false;
          this.locationsVisible = false;
          this.allLocationsVisible = false;
          this.newLocationVisible = false;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = false;
          this.loansVisible = false;
          this.allLoansVisible = false;
          this.newLoanVisible = false;
          this.returnLoanVisible = false;
        },
        // Books
        showAllBooks: function(){
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = false;
          this.booksVisible = true;
          this.locationsVisible = false;
          this.loansVisible = false;
          this.allBooksVisible = true;
          this.newBookVisible = false;
          this.updateBookVisible = false;
          this.deleteBookVisible = false;
          this.allLocationsVisible = false;
          this.newLocationVisible = false;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = false;
          this.allLoansVisible = false;
          this.newLoanVisible = false;
          this.returnLoanVisible = false;
        },
        showNewBook: function(){
          this.newBook = {}
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = false;
          this.booksVisible = true;
          this.locationsVisible = false;
          this.loansVisible = false;
          this.allBooksVisible = false;
          this.newBookVisible = true;
          this.updateBookVisible = false;
          this.deleteBookVisible = false;
          this.allLocationsVisible = false;
          this.newLocationVisible = false;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = false;
          this.allLoansVisible = false;
          this.newLoanVisible = false;
          this.returnLoanVisible = false;
        },
        showUpdateBook: function(){
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = false;
          this.booksVisible = true;
          this.locationsVisible = false;
          this.loansVisible = false;
          this.allBooksVisible = false;
          this.newBookVisible = false;
          this.updateBookVisible = true;
          this.deleteBookVisible = false;
          this.allLocationsVisible = false;
          this.newLocationVisible = false;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = false;
          this.allLoansVisible = false;
          this.newLoanVisible = false;
          this.returnLoanVisible = false;
        },
        showDeleteBook: function(){
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = false;
          this.booksVisible = true;
          this.locationsVisible = false;
          this.loansVisible = false;
          this.allBooksVisible = false;
          this.newBookVisible = false;
          this.updateBookVisible = false;
          this.deleteBookVisible = true;
          this.allLocationsVisible = false;
          this.newLocationVisible = false;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = false;
          this.allLoansVisible = false;
          this.newLoanVisible = false;
          this.returnLoanVisible = false;
        },
        // Locations
        showAllLocations: function(){
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = false;
          this.booksVisible = false;
          this.locationsVisible = true;
          this.loansVisible = false;
          this.allBooksVisible = false;
          this.newBookVisible = false;
          this.updateBookVisible = false;
          this.deleteBookVisible = false;
          this.allLocationsVisible = true;
          this.newLocationVisible = false;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = false;
          this.allLoansVisible = false;
          this.newLoanVisible = false;
          this.returnLoanVisible = false;
        },
        showNewLocation: function(){
          this.newLocation = {}
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = false;
          this.booksVisible = false;
          this.locationsVisible = true;
          this.loansVisible = false;
          this.allBooksVisible = false;
          this.newBookVisible = false;
          this.updateBookVisible = false;
          this.deleteBookVisible = false;
          this.allLocationsVisible = false;
          this.newLocationVisible = true;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = false;
          this.allLoansVisible = false;
          this.newLoanVisible = false;
          this.returnLoanVisible = false;
        },
        showUpdateLocation: function(){
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = false;
          this.booksVisible = false;
          this.locationsVisible = true;
          this.loansVisible = false;
          this.allBooksVisible = false;
          this.newBookVisible = false;
          this.updateBookVisible = false;
          this.deleteBookVisible = false;
          this.allLocationsVisible = false;
          this.newLocationVisible = false;
          this.updateLocationVisible = true;
          this.deleteLocationVisible = false;
          this.allLoansVisible = false;
          this.newLoanVisible = false;
          this.returnLoanVisible = false;
        },
        showDeleteLocation: function(){
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = false;
          this.booksVisible = false;
          this.locationsVisible = true;
          this.loansVisible = false;
          this.allBooksVisible = false;
          this.newBookVisible = false;
          this.updateBookVisible = false;
          this.deleteBookVisible = false;
          this.allLocationsVisible = false;
          this.newLocationVisible = false;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = true;
          this.allLoansVisible = false;
          this.newLoanVisible = false;
          this.returnLoanVisible = false;
      },
        // Loans
        showAllLoans: function(){
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = false;
          this.booksVisible = false;
          this.locationsVisible = false;
          this.loansVisible = true;
          this.allBooksVisible = false;
          this.newBookVisible = false;
          this.updateBookVisible = false;
          this.deleteBookVisible = false;
          this.allLocationsVisible = false;
          this.newLocationVisible = false;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = false;
          this.allLoansVisible = true;
          this.newLoanVisible = false;
          this.returnLoanVisible = false;
        },
        showNewLoan: function(){
          this.newLoan = {}
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = false;
          this.booksVisible = false;
          this.locationsVisible = false;
          this.loansVisible = true;
          this.allBooksVisible = false;
          this.newBookVisible = false;
          this.updateBookVisible = false;
          this.deleteBookVisible = false;
          this.allLocationsVisible = false;
          this.newLocationVisible = false;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = false;
          this.allLoansVisible = false;
          this.newLoanVisible = true;
          this.returnLoanVisible = false;
        },
        showReturnLoan: function(){
          this.navbarVisible = true;
          this.loginVisible = false;
          this.homeVisible = false;
          this.booksVisible = false;
          this.locationsVisible = false;
          this.loansVisible = true;
          this.allBooksVisible = false;
          this.newBookVisible = false;
          this.updateBookVisible = false;
          this.deleteBookVisible = false;
          this.allLocationsVisible = false;
          this.newLocationVisible = false;
          this.updateLocationVisible = false;
          this.deleteLocationVisible = false;
          this.allLoansVisible = false;
          this.newLoanVisible = false;
          this.returnLoanVisible = true;
        },
        // Get Activities
        getActivities: function() {
          this.loading = true;
          this.$http.get('/api/activities/', {headers: {Authorization: `JWT ${this.jwt}`}})
              .then((response) => {
                this.activities = response.data;
                // to trim down the activities list
                // this.activities = this.activities.slice(this.activities.length - 10, this.activities.length)
                this.loading = false;
              })
              .catch((err) => {
               this.loading = false;
               console.log(err);
              })
        },
        // CRUD methods
        // Books
        addBook: function() {
          this.loading = true;
          this.newBook.username = this.username;
          this.$http.post('/api/books/',this.newBook, {headers: {Authorization: `JWT ${this.jwt}`}})
              .then((response) => {
                this.loading = false;
                this.getBooks();
                this.showAllBooks();
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        getBooks: function() {
          this.loading = true;
          this.$http.get('/api/books/', {headers: {Authorization: `JWT ${this.jwt}`}})
              .then((response) => {
                this.books = response.data;
                this.loading = false;
              })
              .catch((err) => {
               this.loading = false;
               console.log(err);
              })
        },
        bookDetails: function(book){
            this.book = book;
            this.showUpdateBook();
        },
        updateBook: function(book) {
          this.loading = true;
          this.$http.put(`/api/books/${book.id}/`, book, {headers: {Authorization: `JWT ${this.jwt}`}})
              .then((response) => {
                this.loading = false;
                this.book = {};
                this.getBooks();
                this.showAllBooks();
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        deleteBook: function(book){
          confirmation = confirm('Delete book "' + book.title + '" ?');
          if (confirmation == true){
              this.loading = true;
              this.$http.delete(`/api/books/${book.id}/`, {headers: {Authorization: `JWT ${this.jwt}`}})
                  .then((response) => {
                    this.loading = false;
                    this.getBooks();
                    this.showAllBooks();
                  })
                  .catch((err) => {
                    this.loading = false;
                    console.log(err);
                  })
          }
        },
        // Locations
        addLocation: function(location) {
          this.loading = true;
          location.username = this.username;
          this.$http.post('/api/locations/', location, {headers: {Authorization: `JWT ${this.jwt}`}})
              .then((response) => {
                this.newLocation = {};
                this.loading = true;
                this.getLocations();
                this.showAllLocations();
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        getLocations: function() {
          this.loading = true;
          this.$http.get('/api/locations/', {headers: {Authorization: `JWT ${this.jwt}`}})
              .then((response) => {
                this.locations = response.data;
                this.loading = false;
              })
              .catch((err) => {
               this.loading = false;
               console.log('[!!!] ' + err);
              })
        },
        locationDetails: function(location){
          this.location = location;
          this.showUpdateLocation();
        },
        updateLocation: function(location) {
          this.loading = true;
          this.$http.put(`/api/locations/${location.id}/`, location, {headers: {Authorization: `JWT ${this.jwt}`}})
              .then((response) => {
                this.loading = false;
                this.location = {};
                this.getLocations();
                this.showAllLocations();
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        deleteLocation: function(location){
          confirmation = confirm('Delete Location "' + location.room + '" ?');
          if (confirmation == true){
              this.loading = true;
              this.$http.delete(`/api/locations/${location.id}/`, {headers: {Authorization: `JWT ${this.jwt}`}})
                  .then((response) => {
                    this.loading = false;
                    this.getLocations();
                    this.showAllLocations();
                  })
                  .catch((err) => {
                    this.loading = false;
                    console.log(err);
                  })
          }
        },
        // Loans
        addLoan: function(loan) {
          this.loading = true;
          // set the book as loaned
          this.$http.get(`/api/books/${loan.book}/`, {headers: {Authorization: `JWT ${this.jwt}`}})
            .then((response) => {
              book = response.data;
              book.loaned = true;
              this.$http.put(`/api/books/${book.id}/`, book, {headers: {Authorization: `JWT ${this.jwt}`}})
                .then((response) => {
                  this.getBooks();
                })
                .catch((err) => {
                  this.loading = false;
                  console.log(err);
              });
            })
            .catch((err) => {
            this.loading = false;
            console.log(err);
          });          
          // register loan
          loan.lender = this.username;
          this.$http.post('/api/loans/', loan, {headers: {Authorization: `JWT ${this.jwt}`}})
              .then((response) => {
                this.newLoan = {};
                this.loading = false;
                this.getLoans();
                this.showAllLoans();
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        getLoans: function() {
          this.loading = true;
          this.$http.get('/api/loans/', {headers: {Authorization: `JWT ${this.jwt}`}})
              .then((response) => {
                this.loans = response.data;
                this.loading = false;
              })
              .catch((err) => {
               this.loading = false;
               console.log(err);
              })
         },
        loanDetails: function(loan){
          this.loan = loan;
          this.showUpdateLoan();
        },
        returnLoan: function(loan) {
          confirmation = confirm('Book "' + loan.book + '" returned?');
          if (confirmation == true){
            this.loading = true;
            // set the book as loaned
            this.$http.get(`/api/books/${loan.book}/`, {headers: {Authorization: `JWT ${this.jwt}`}})
              .then((response) => {
                book = response.data;
                book.loaned = false;
                this.$http.put(`/api/books/${book.id}/`, book, {headers: {Authorization: `JWT ${this.jwt}`}})
                  .then((response) => {
                    this.getBooks();
                    this.showAllLoans();
                  })
                  .catch((err) => {
                    this.loading = false;
                    console.log(err);
                });
              })
              .catch((err) => {
              this.loading = false;
              console.log(err);
            });
            // register return
            loan.return_date = new Date().toISOString();
            this.$http.put(`/api/loans/${loan.id}/`, loan)
                .then((response) => {
                  this.loading = false;
                  this.loan = {};
                  this.getLoans();
                  this.showAllLoans();
                })
                .catch((err) => {
                  this.loading = false;
                  console.log(err);
                })
            }
        },
    },
    mounted: function(){
      if (localStorage.getItem("jwt") === 'null'){
        this.showLogin();
      }
      else{
        this.jwt = localStorage.jwt;
        this.username = localStorage.username;
        this.getBooks();
        this.getLocations();
        this.getLoans();
        this.getActivities();
        this.showHome();
      }
    }
})