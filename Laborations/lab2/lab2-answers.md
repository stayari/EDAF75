1) Se figur "Lab2 EDAF75.jpg"
2) Se figur "Lab2 EDAF75.jpg"
3)
4)
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
