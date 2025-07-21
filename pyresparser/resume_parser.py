# Author: Taha Hasan

import os
import multiprocessing as mp
import io
import spacy
import pprint
from spacy.matcher import Matcher
from . import utils


class ResumeParser(object):

    def __init__(
        self,
        resume,
        skills_file=None,
        custom_regex=None
    ):
        nlp = spacy.load('en_core_web_sm')
        # custom_nlp = spacy.load(os.path.dirname(os.path.abspath(__file__)))
        self.__skills_file = skills_file
        self.__custom_regex = custom_regex
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            'name': None,
            'email': None,
            'mobile_number': None,
            'skills': None,
            'college_name': None,
            'degree': None,
            'designation': None,
            'experience': None,
            'company_names': None,
            'no_of_pages': None,
            'total_experience': None,
        }
        self.__resume = resume
        if not isinstance(self.__resume, io.BytesIO):
            ext = os.path.splitext(self.__resume)[1].split('.')[1]
        else:
            ext = self.__resume.name.split('.')[1]
        self.__text_raw = utils.extract_text(self.__resume, '.' + ext)
        self.__text = ' '.join(self.__text_raw.split())
        self.__nlp = nlp(self.__text)
        # self.__custom_nlp = custom_nlp(self.__text_raw)
        self.__custom_nlp = self.__nlp 
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()

    def get_extracted_data(self):
        return self.__details

    def __get_basic_details(self):
        # cust_ent = utils.extract_entities_wih_custom_model(
        #                     self.__custom_nlp
        #                 )
        name = utils.extract_name(self.__nlp, matcher=self.__matcher)
        email = utils.extract_email(self.__text)
        mobile = utils.extract_mobile_number(self.__text, self.__custom_regex)
        skills = utils.extract_skills(
                    self.__nlp,
                    self.__noun_chunks,
                    self.__skills_file
                )

        # Use the new robust function
        entities = utils.robust_extract_entity_sections(self.__text_raw)

        # extract name
        self.__details['name'] = name

        # extract email
        self.__details['email'] = email

        # extract mobile number
        self.__details['mobile_number'] = mobile

        # extract skills
        self.__details['skills'] = skills

        # extract education
        education_info = entities.get('education')
        if education_info:
            self.__details['education'] = education_info
            self.__details['college_name'] = ' '.join(education_info)
            # Simple heuristic for degree, can be improved
            for line in education_info:
                if 'bachelor' in line.lower() or 'master' in line.lower() or 'phd' in line.lower() or 'b.e' in line.lower():
                    self.__details['degree'] = line
                    break

        # extract experience
        experience_info = entities.get('experience')
        if experience_info:
            self.__details['experience'] = experience_info
            
            # extract total experience
            experience_months = utils.get_total_experience(experience_info)
            if experience_months:
                self.__details['total_experience'] = round(experience_months / 12, 2)

        # extract projects
        projects_info = entities.get('projects')
        if projects_info:
            self.__details['projects'] = projects_info
            
        # extract certifications
        certifications_info = entities.get('certifications')
        if certifications_info:
            self.__details['certifications'] = certifications_info

        # extract designation and company names from experience
        # (This is a placeholder, can be improved with more advanced parsing)
        if experience_info:
            # Simple heuristic: first line is designation at first company
            self.__details['designation'] = experience_info[0]
            self.__details['company_names'] = [line for line in experience_info if any(keyword in line.lower() for keyword in ['ltd', 'inc', 'llc', 'pvt'])]


        # extract number of pages
        self.__details['no_of_pages'] = utils.get_number_of_pages(self.__resume)

        return


def resume_result_wrapper(resume):
    parser = ResumeParser(resume)
    return parser.get_extracted_data()


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())

    resumes = []
    data = []
    for root, directories, filenames in os.walk('resumes/'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    results = [
        pool.apply_async(
            resume_result_wrapper,
            args=(x,)
        ) for x in resumes
    ]

    results = [p.get() for p in results]

    pprint.pprint(results)
