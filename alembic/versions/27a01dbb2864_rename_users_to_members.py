from alembic import op
import sqlalchemy as sa

revision = "27a01dbb2864"
down_revision = "9e8f7f02d0e4"
branch_labels = None
depends_on = None


def upgrade():

    # rename users -> members
    op.rename_table("users", "members")

    # rename index
    op.execute(
        "ALTER INDEX ix_users_id RENAME TO ix_members_id"
    )

    op.execute(
        "ALTER INDEX ix_users_member_id RENAME TO ix_members_member_id"
    )

    # hapus registrations
    op.drop_index(
        "ix_registrations_dkm_group",
        table_name="registrations"
    )

    op.drop_index(
        "ix_registrations_full_name",
        table_name="registrations"
    )

    op.drop_index(
        "ix_registrations_id",
        table_name="registrations"
    )

    op.drop_table("registrations")


def downgrade():

    raise NotImplementedError(
        "Downgrade belum dibuat"
    )