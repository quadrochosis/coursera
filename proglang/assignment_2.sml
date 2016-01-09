(* Second programming assignment for Programming Languages Coursera course *)

(* Problem 1 *)
(* if you use this function to compare two strings (returns true if the same
   string), then you avoid several of the functions in problem 1 having
   polymorphic types that may be confusing *)
fun same_string(s1 : string, s2 : string) =
    s1 = s2

fun all_except_option(_, []) = NONE
  | all_except_option (str, x::xs) =
        if same_string (str, x)
        then
          SOME xs
        else
          case all_except_option (str, xs) of
               NONE   => NONE
             | SOME y => SOME (x::y)

fun get_substitutions1([], _) = []
  | get_substitutions1(x::xs, str) =
      case all_except_option (str, x) of
           NONE   => get_substitutions1 (xs, str)
         | SOME y => y @ get_substitutions1 (xs, str)

fun get_substitutions2(lst, str) =
  let
    fun aux([], acc) = acc
      | aux(x::xs, acc) =
          case all_except_option (str, x) of
               NONE   => aux(xs, acc)
             | SOME y => aux(xs, y @ acc)
  in
    aux(lst, [])
  end

fun similar_names(strs, {first=f,middle=m,last=l}) =
    let 
	fun aux([]) = []
          | aux(x::xs) = {first=x,middle=m,last=l}::aux(xs)
    in
        {first=f,middle=m,last=l}::aux(get_substitutions2(strs, f))
    end

(* Problem 2 *)
(* you may assume that Num is always used with values 2, 3, ..., 10
   though it will not really come up *)
datatype suit = Clubs | Diamonds | Hearts | Spades
datatype rank = Jack | Queen | King | Ace | Num of int 
type card = suit * rank

datatype color = Red | Black
datatype move = Discard of card | Draw 

exception IllegalMove

fun card_color(suit, rank) =
	case suit of
		  Clubs => Black
		| Spades => Black
		| Hearts => Red
		| Diamonds => Red

fun card_value(suit, rank) =
	case rank of
		  Num num => num
		| Ace => 11
		| _ => 10

fun remove_card([], _, e): card list = raise e
  | remove_card (c::cs, card, e) = if c = card then cs else c::remove_card(cs, card, e)

fun all_same_color(cs: card list) =
    case cs of
        [] => true
      | c1::[] => true
      | c1::c2::cs => card_color(c1) = card_color(c2) andalso all_same_color(c2::cs)
                                         
fun sum_cards(cs: card list) = 
    let
        fun sum([], acc: int) = acc
	  | sum(c::cs, acc)  = sum(cs, acc + card_value(c))
    in
        sum(cs, 0)
    end
                
fun score(cs: card list, goal: int) =
        let
                val sum = sum_cards(cs);
                val ps = if sum > goal then 3*(sum - goal) else (goal - sum)
        in
                if all_same_color(cs) then ps div 2 else ps
        end

fun officiate(cards, moves, goal) = 
    let 
	fun aux(_, [], held) = score(held, goal)
	  | aux(cards: card list, moves, held) = 
            case(cards, moves) of 
		([], Draw::ms) =>  score(held, goal)
              | ([], Discard c :: ms) => raise IllegalMove 
              | (c :: cs, Draw :: ms) => if sum_cards(c::held) > goal then score(c::held, goal) else aux(cs, ms, c :: held)
              | (_, Discard c :: ms) => aux(remove_card(cards, c, IllegalMove), ms, held)
    in
        aux(cards, moves, [])
    end