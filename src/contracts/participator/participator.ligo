type participant is record
  name : string;
  balance : tez;
end
type participant_map is big_map (address, participant)
type storage is record
  participants : participant_map;
  owner : address;
end
type add_participant_params is record
  address : address;
  name : string;
end

type action is
| AddParticipant of add_participant_params
| Participate of unit

function add_participant (const x : add_participant_params ; var s : storage) : storage is
  block {
    if sender =/= s.owner then
      failwith("ERROR_ONLY_OWNER_CAN_ADD_PARTICIPANT");
    else
      case s.participants[x.address] of
        | None -> s.participants[x.address] := record name = x.name; balance = amount; end
        | Some(x) -> failwith("ERROR_CANNOT_ADD_DUPLICATE_PARTICIPANT")
      end
  } with s

function participate (var s : storage) : storage is
  block {
    case s.participants[sender] of
      | None -> failwith("ERROR_ONLY_REGISTERED_PARTICIPANTS_CAN_PARTICIPATE")
      | Some(x) -> block {
          x.balance := x.balance + amount;
          s.participants[sender] := x;
        }
    end
  } with s

function main (const a : action ; var s : storage) : (list(operation) * storage) is
  block { skip } with ((nil : list(operation)),
  case a of
  | AddParticipant (x) -> add_participant (x, s)
  | Participate (x) -> participate (s)
  end)

