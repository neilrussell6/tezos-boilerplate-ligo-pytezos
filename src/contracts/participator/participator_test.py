"""Participator smart contract tests"""
from decimal import Decimal

import pytest
from pytezos import ContractInterface, MichelsonRuntimeError

from src.contracts.participator.participator_constants import (
    ERROR_CANNOT_ADD_DUPLICATE_PARTICIPANT,
    ERROR_ONLY_OWNER_CAN_ADD_PARTICIPANT,
    ERROR_ONLY_REGISTERED_PARTICIPANTS_CAN_PARTICIPATE,
)


@pytest.fixture
def participator():
    """Return configured instance of Participator smart contract"""
    contract_path = 'src/contracts/participator/participator.tz'
    instance = ContractInterface.create_from(contract_path)
    instance.maxDiff = None
    return instance


owner_address = 'tz1bVNHSrD3sneJXQToWzzJ72eNmon2FH1D9'


# -----------------------------------------
# tests
# -----------------------------------------

def test_add_participant_allows_owner_to_add_participant(participator):
    """Should allow owner to add participant with initial amount."""
    participant_address = 'tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp'

    # given ... a Participator contract instance with owner set
    instance = participator

    # when
    # ... we add a participant as the owner
    # then
    # ... should succeed
    result = instance \
        .addParticipant(address=participant_address, name='ONE') \
        .with_amount(Decimal('1')) \
        .result(
            storage={'participants': {}, 'owner': owner_address},
            sender=owner_address,
        )
    # ... adding the participant
    assert len(result.big_map_diff['participants']) == 1
    assert participant_address in result.big_map_diff['participants']
    # ... with the provided amount as their initial value
    assert result.big_map_diff['participants'][participant_address]['name'] == 'ONE'
    assert result.big_map_diff['participants'][participant_address]['balance'] == Decimal('1')


def test_add_participant_not_allow_adding_duplicate_participant(participator):
    """Should not allow adding duplicate participants."""
    participant_address = 'tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp'

    # given
    # ... a Participator contract instance with owner set
    # ... that already has a participant
    instance = participator
    participants = {participant_address: {'name': 'ONE', 'balance': Decimal('1')}}

    # when
    # ... we attempt to re-add an existing participant as the owner
    # then
    # ... should fail
    with pytest.raises(MichelsonRuntimeError, match=ERROR_CANNOT_ADD_DUPLICATE_PARTICIPANT):
        result = instance \
            .addParticipant(address=participant_address, name='ONE') \
            .with_amount(Decimal('1')) \
            .result(
                storage={'participants': participants, 'owner': owner_address},
                sender=owner_address,
            )
        # ... not adding an additional participant or affecting existing participant
        assert len(result.big_map_diff['participants']) == 1
        assert result.big_map_diff['participants'][participant_address]['name'] == 'ONE'
        assert result.big_map_diff['participants'][participant_address]['balance'] == Decimal('1')


def test_add_participant_does_not_allow_non_owner_to_add_participant(participator):
    """Should not allow non-owner to add participant."""
    participant_address = 'tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp'
    not_owner_address = 'tz1fxvhgsbRxYKQ4gZ8U3LY1DHxdByjwzdHW'

    # given ... a Participator contract instance with owner set
    instance = participator

    # when
    # ... we attempt to add a participant as not the owner
    # then
    # ... should fail
    with pytest.raises(MichelsonRuntimeError, match=ERROR_ONLY_OWNER_CAN_ADD_PARTICIPANT):
        result = instance \
            .addParticipant(address=participant_address, name='ONE') \
            .with_amount(Decimal('1')) \
            .result(
                storage={'participants': {}, 'owner': owner_address},
                sender=not_owner_address,
            )
        # ... not adding participant
        assert len(result.big_map_diff['participants']) == 0
        assert participant_address not in result.big_map_diff['participants']


def test_participate_allows_participants_to_participate(participator):
    """Should allow participants to participate, incrementing their value."""
    registered_participant_address = 'tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp'

    # given
    # ... a Participator contract instance with owner set
    # ... that already has a participant
    instance = participator
    participants = {registered_participant_address: {'name': 'ONE', 'balance': Decimal('1')}}

    # when
    # ... we participate as a registered participant
    # then
    # ... should succeed
    # TODO: find out why we need to pass an address to participate  # noqa: T000
    # TODO: I would expect this to work participate() or participate(None)  # noqa: T000
    result = instance \
        .participate('tz1fxvhgsbRxYKQ4gZ8U3LY1DHxdByjwzdHW') \
        .with_amount(Decimal('3')) \
        .result(
            storage={'participants': participants, 'owner': owner_address},
            sender=registered_participant_address,
        )
    # ... incrementing our participant value
    assert result.big_map_diff['participants'][registered_participant_address]['balance'] == Decimal('4')


def test_participate_does_not_allow_unregistered_user_to_participate(participator):
    """Should not allow unregistered user to participate."""
    registered_participant_address = 'tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp'
    unregistered_participant_address = 'tz1fxvhgsbRxYKQ4gZ8U3LY1DHxdByjwzdHW'

    # given
    # ... a Participator contract instance with owner set
    # ... that already has a participant
    instance = participator
    participants = {registered_participant_address: {'name': 'ONE', 'balance': Decimal('1')}}

    # when
    # ... we attempt to participate as a unregistered participant
    # then
    # ... should fail
    with pytest.raises(MichelsonRuntimeError, match=ERROR_ONLY_REGISTERED_PARTICIPANTS_CAN_PARTICIPATE):
        instance \
            .participate(unregistered_participant_address) \
            .with_amount(Decimal('3')) \
            .result(
                storage={'participants': participants, 'owner': owner_address},
                sender=unregistered_participant_address,
            )
