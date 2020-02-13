1) Se figur "Lab2 EDAF75.jpg"
2) Se figur "Lab2 EDAF75.jpg"
3) Se figur "Lab2 EDAF75.jpg"
4)
    a) theater - shows    Naturalkey: th_name
        shows - movies    Naturalkey: IMDB_key
        shows - tickets   Naturalkey: th_name, IMDB_key, start_time, start_date
        tickets - customers Naturalkey: user_name 
    b)  Yes, th_name.
        For the relation tickets-shows the start_time/start_date might change but then you would create a new show instead which means we won't have a problem.
    c) Yes the tickets is a weak entity since this entity only ties a customer to a show

    d)



5)
6)
    theaters(_th_name_, capacity)
    shows(/_IMDB_code_/,_start_time_, _start_time_, _start_date_, /_th_name_/)
    movies(_IMDB_code_, title, duration, year)
    tickets(_ticket_id_, th_name, IMDB_key, start_time, start_date, /user_id/)
    customers(_user_id_, full_name, password)
7)
    a) Joining theaters, shows and tickets group by shows and counting rows in each group. Compare that count with the capacity of the respective theaters.

    b) Having a counter as an attribute of the show, decreasing it each time a ticket is bought. The problem with this solution is that we will run in to concurrancy problems when multiple actors try to create a ticket simultaneously. But the uppside of this solution is in a case were there would be alot of instances to count this would be faster. However this is not applicaple in this situation since the tickets bought for a show won't be to big of a number.  
