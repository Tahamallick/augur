""" Updating materialized views and associated indices

Revision ID: 26
Revises: 25
Create Date: 2023-08-23 18:17:22.651191

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = '27'
down_revision = '26'
branch_labels = None
depends_on = None


def upgrade():

    mview_keys_27()

def downgrade():

    upgrade=False

    mview_keys_27(upgrade)

def mview_keys_27(upgrade=True):

   if upgrade:
      conn = op.get_bind() 
      conn.execute(text("""
                        
      DROP INDEX if exists "pr_ID_prs_table"; 
      DROP INDEX if exists "pr_id_pr_files"; 
      DROP INDEX if exists "pr_id_pr_reviews"; 
                        
      
      CREATE INDEX "pr_ID_prs_table" ON "augur_data"."pull_requests" USING btree (
       "pull_request_id" "pg_catalog"."int8_ops" ASC NULLS LAST
        );

        CREATE INDEX "pr_id_pr_files" ON "augur_data"."pull_request_files" USING btree (
        "pull_request_id" "pg_catalog"."int8_ops" ASC NULLS LAST
        );

        CREATE INDEX "pr_id_pr_reviews" ON "augur_data"."pull_request_reviews" USING btree (
        "pull_request_id" "pg_catalog"."int8_ops" ASC NULLS LAST
        );"""))


      conn.execute(text("""COMMIT;"""))