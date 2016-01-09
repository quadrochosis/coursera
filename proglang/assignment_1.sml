(* First programming assignment for Programming Languages Coursera course *)

(* You will write 11 SML functions (and tests for them) related to calendar dates. In all problems, a “date”
is an SML value of type int*int*int, where the first part is the year, the second part is the month, and
the third part is the day. A “reasonable” date has a positive year, a month between 1 and 12, and a day no
greater than 31 (or less depending on the month). Your solutions need to work correctly only for reasonable
dates, but do not check for reasonable dates (that is a challenge problem) and many of your functions will
naturally work correctly for some/all non-reasonable dates. A “day of year” is a number from 1 to 365
where, for example, 33 represents February 2. (We ignore leap years except in one challenge problem.) *)

(* 1. Write a function is_older that takes two dates and evaluates to true or false. It evaluates to true if
the first argument is a date that comes before the second argument. (If the two dates are the same,
the result is false.) *)
fun is_older (first : (int*int*int), second : (int*int*int)) =
	(#1 first * 365) + (#2 first * 30) + #3 first < (#1 second * 365) + (#2 second * 30) + #3 second

(* 2. Write a function number_in_month that takes a list of dates and a month (i.e., an int) and returns
how many dates in the list are in the given month. *)
fun number_in_month (dates_list : (int*int*int) list, month : int) =
	if null (dates_list)
	then 0
	else
		if #2 (hd dates_list) = month
		then 1 + number_in_month(tl dates_list, month)
		else number_in_month(tl dates_list, month)

(* 3. Write a function number_in_months that takes a list of dates and a list of months (i.e., an int list)
and returns the number of dates in the list of dates that are in any of the months in the list of months.
Assume the list of months has no number repeated. Hint: Use your answer to the previous problem. *)
fun number_in_months (dates_list : (int*int*int) list, months : int list) =
	if null (months)
	then 0
	else
		number_in_month(dates_list, hd months) + number_in_months(dates_list, tl months)

(* 4. Write a function dates_in_month that takes a list of dates and a month (i.e., an int) and returns a
list holding the dates from the argument list of dates that are in the month. The returned list should
contain dates in the order they were originally given. *)
fun dates_in_month (dates_list : (int*int*int) list, month : int) =
	if null (dates_list)
	then []
	else
		if #2 (hd dates_list) = month
		then hd dates_list :: dates_in_month(tl dates_list, month)
		else dates_in_month(tl dates_list, month)

(* 5. Write a function dates_in_months that takes a list of dates and a list of months (i.e., an int list)
and returns a list holding the dates from the argument list of dates that are in any of the months in
the list of months. Assume the list of months has no number repeated. Hint: Use your answer to the
previous problem and SML’s list-append operator (@). *)
fun dates_in_months (dates_list : (int*int*int) list, months : int list) =
	if null (months)
	then []
	else
		dates_in_month(dates_list, hd months) @ dates_in_months(dates_list, tl months)

(* 6. Write a function get_nth that takes a list of strings and an int n and returns the n th element of the
list where the head of the list is 1 st . Do not worry about the case where the list has too few elements:
your function may apply hd or tl to the empty list in this case, which is okay. *)
fun get_nth (string_list : string list, n : int) =
	if n = 1
	then hd string_list
	else get_nth(tl string_list, n - 1)

(* 7. Write a function date_to_string that takes a date and returns a string of the form January 20, 2013
(for example). Use the operator ^ for concatenating strings and the library function Int.toString
for converting an int to a string. For producing the month part, do not use a bunch of conditionals.
Instead, use a list holding 12 strings and your answer to the previous problem. For consistency, put a
comma following the day and use capitalized English month names: January, February, March, April,
May, June, July, August, September, October, November, December. *)
fun date_to_string (date : (int*int*int)) =
	let val months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	in
		get_nth(months_list, #2 date) ^ " " ^ Int.toString(#3 date) ^ ", " ^ Int.toString(#1 date)
	end

(* 8. Write a function number_before_reaching_sum that takes an int called sum, which you can assume
is positive, and an int list, which you can assume contains all positive numbers, and returns an int.
You should return an int n such that the first n elements of the list add to less than sum, but the first
n + 1 elements of the list add to sum or more. Assume the entire list sums to more than the passed in
value; it is okay for an exception to occur if this is not the case. *)
fun number_before_reaching_sum (sum : int, number_list : int list) =
	let fun search_list(i : int, list_sum : int, vs : int list) = 
	    if list_sum + hd vs >= sum
	    then i
	    else search_list(i + 1, list_sum + hd vs, tl vs)
    in 
	search_list(0, 0, number_list)
    end

(* 9. Write a function what_month that takes a day of year (i.e., an int between 1 and 365) and returns
what month that day is in (1 for January, 2 for February, etc.). Use a list holding 12 integers and your
answer to the previous problem. *)
fun what_month (day : int) =
	let val days_in_months = [31,28,31,30,31,30,31,31,30,31,30,31]
	in
		number_before_reaching_sum(day, days_in_months) + 1
	end

(* 10. Write a function month_range that takes two days of the year day1 and day2 and returns an int list
[m1,m2,...,mn] where m1 is the month of day1, m2 is the month of day1+1, ..., and mn is the month
of day day2. Note the result will have length day2 - day1 + 1 or length 0 if day1>day2. *)
fun month_range (first : int, second : int) =
	if first > second
	then []
	else
		(what_month(first)) :: month_range(first + 1, second)

(* 11. Write a function oldest that takes a list of dates and evaluates to an (int*int*int) option. It
evaluates to NONE if the list has no dates and SOME d if the date d is the oldest date in the list. *)
fun oldest (dates_list : (int*int*int) list) =
	if null (dates_list)
	then NONE
	else let
		fun older_date(dates_list : (int*int*int) list) =
			if null (tl dates_list)
			then hd dates_list
			else let val ans = older_date(tl dates_list)
				in
					if is_older(hd dates_list, ans)
					then hd dates_list
					else ans
				end
	in
		SOME (older_date(dates_list))
	end