"""
data types for 2011/01 Helios
"""

from helios_server.helios.datatypes import LDObject, arrayOf, DictObject, ListObject


class Trustee(LDObject):
    """
    a trustee
    """

    FIELDS = [
        "uuid",
        "public_key",
        "public_key_hash",
        "pok",
        "decryption_factors",
        "decryption_proofs",
        "email",
    ]
    STRUCTURED_FIELDS = {
        "pok": "pkc/elgamal/DiscreteLogProof",
        "public_key": "pkc/elgamal/PublicKey",
        "decryption_factors": arrayOf(arrayOf("core/BigInteger")),
        "decryption_proofs": arrayOf(arrayOf("legacy/EGZKProof")),
    }

    # removed some public key processing for now


class Election(LDObject):
    FIELDS = [
        "uuid",
        "questions",
        "name",
        "short_name",
        "description",
        "voters_hash",
        "openreg",
        "frozen_at",
        "public_key",
        "cast_url",
        "use_advanced_audit_features",
        "use_voter_aliases",
        "voting_starts_at",
        "voting_ends_at",
    ]

    STRUCTURED_FIELDS = {
        "public_key": "pkc/elgamal/PublicKey",
        "voting_starts_at": "core/Timestamp",
        "voting_ends_at": "core/Timestamp",
        "frozen_at": "core/Timestamp",
        "questions": "2011/01/Questions",
    }


class Voter(LDObject):
    FIELDS = ["election_uuid", "uuid", "voter_type", "voter_id_hash", "name"]

    ALIASED_VOTER_FIELDS = ["election_uuid", "uuid", "alias_num"]


class EncryptedAnswer(LDObject):
    FIELDS = ["choices", "individual_proofs", "overall_proof", "randomness", "answer"]
    STRUCTURED_FIELDS = {
        "choices": arrayOf("pkc/elgamal/EGCiphertext"),
        "individual_proofs": arrayOf("pkc/elgamal/DisjunctiveProof"),
        "overall_proof": "pkc/elgamal/DisjunctiveProof",
        "randomness": "core/BigInteger"
        # answer is not a structured field, it's an as-is integer
    }

class ShortCastVote(LDObject):
    FIELDS = ["cast_at", "voter_uuid", "voter_hash", "vote_hash"]
    STRUCTURED_FIELDS = {"cast_at": "core/Timestamp"}


class CastVote(LDObject):
    FIELDS = ["vote", "cast_at", "voter_uuid", "voter_hash", "vote_hash"]
    STRUCTURED_FIELDS = {"cast_at": "core/Timestamp", "vote": "legacy/EncryptedVote"}

    @property
    def short(self):
        return self.instantiate(self.wrapped_obj, datatype="2011/01/ShortCastVote")

Questions = arrayOf("2011/01/Question")


class Question(LDObject):
    FIELDS = [
        "answer_urls",
        "answers",
        "choice_type",
        "max",
        "min",
        "question",
        "result_type",
        "short_name",
        "tally_type",
    ]
