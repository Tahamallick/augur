from datetime import datetime
from augur.application.db.models import *
from augur.application.db.lib import get_value, bulk_insert_dicts
from augur.application.db.util import execute_session_query
from augur.tasks.git.dependency_libyear_tasks.libyear_util.util import get_deps_libyear_data
from augur.tasks.git.util.facade_worker.facade_worker.utilitymethods import get_absolute_repo_path

def deps_libyear_model(logger, session, repo_id,repo_git,repo_group_id):
        """ Data collection and storage method
        """
        logger.info(f"This is the libyear deps model repo: {repo_git}")

        #result = re.search(r"https:\/\/(github\.com\/[A-Za-z0-9 \- _]+\/)([A-Za-z0-9 \- _ .]+)$", repo_git).groups()

        #relative_repo_path = f"{repo_group_id}/{result[0]}{result[1]}"
        query = session.query(Repo).filter(
            Repo.repo_git == repo_git)
        
        result = execute_session_query(query, 'one')
        
        absolute_repo_path = get_absolute_repo_path(get_value("Facade", "repo_directory"),repo_id,result.repo_path,result.repo_name)
        #config.get_section("Facade")['repo_directory'] + relative_repo_path#self.config['repo_directory'] + relative_repo_path

        generate_deps_libyear_data(logger, repo_id, absolute_repo_path)


def generate_deps_libyear_data(logger, repo_id, path):
        """Scans for package files and calculates libyear
        :param repo_id: Repository ID
        :param path: Absolute path of the Repostiory
        """
        date_scanned = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        logger.info('Searching for deps in repo')
        logger.info(f'Repo ID: {repo_id}, Path: {path}')

        deps = get_deps_libyear_data(path,logger)

        if not deps:
            logger.info(f"No deps found for repo {repo_id} on path {path}")
            return

        to_insert = []
        for dep in deps:
            repo_deps = {
                'repo_id': repo_id,
                'name' : dep['name'],
                'requirement' : dep['requirement'],
                'type' : dep['type'],
                'package_manager' : dep['package'],
                'current_verion' : dep['current_version'],
                'latest_version' : dep['latest_version'],
                'current_release_date' : dep['current_release_date'],
                'latest_release_date' : dep['latest_release_date'],
                'libyear' : dep['libyear'],
                'tool_source': 'deps_libyear',
                'tool_version': '0.44.3',
                'data_source': 'git',
                'data_collection_date': date_scanned
            }

            #result = self.db.execute(self.repo_deps_libyear_table.insert().values(repo_deps))
            #self.logger.info(f"Added dep: {result.inserted_primary_key}")
            #insert_statement = s.sql.text("""
            #    INSERT INTO "repo_deps_libyear" ("repo_id","name","requirement","type","package_manager","current_verion","latest_version","current_release_date","latest_release_date","libyear","tool_source","tool_version","data_source","data_collection_date")
            #    VALUES (:repo_id, :name,:requirement,:type,:package_manager,:current_verion,:latest_version,:current_release_date,:latest_release_date,:libyear,:tool_source,:tool_version,:data_source, :data_collection_date)
            #""").bindparams(**repo_deps)
#
            #session.execute_sql(insert_statement)
            to_insert.append(repo_deps)

        bulk_insert_dicts(logger, to_insert, RepoDepsLibyear, ["repo_id","name","data_collection_date"])
