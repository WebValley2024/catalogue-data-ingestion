from .models import add_all_data, SampleModel, Earthquake, GRB, TGF, SWE, GMS


def update():
    SampleModel.prova()
    Earthquake.add_data()
    GRB.add_data()
    TGF.add_data()
    SWE.add_data()
    GMS.add_data()
    #add_all_data()