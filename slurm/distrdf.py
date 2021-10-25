from dask_jobqueue import SLURMCluster
from distributed import Client
from dask import delayed

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cores", type=int, default=4)
parser.add_argument("-N", "--Nodes", type=int, default=1)
args = parser.parse_args()

cluster = SLURMCluster(memory='{}g'.format(4*args.cores),
                       processes=args.cores,
                       cores=args.cores,
                       queue='photon',
                       header_skip=['-n 1', '-N 1'],
                       job_extra=['--ntasks-per-node 1', '-N {}'.format(args.Nodes)])

cluster.scale(jobs=1)
client = Client(cluster)


import ROOT
ROOT.gROOT.SetBatch(True)

RDataFrame = ROOT.RDF.Experimental.Distributed.Dask.RDataFrame



def dimuonSpectrum(df):
    # Select events with exactly two muons
    df_2mu = df.Filter("nMuon == 2", "Events with exactly two muons")

    # Select events with two muons of opposite charge
    df_os = df_2mu.Filter(
        "Muon_charge[0] != Muon_charge[1]", "Muons with opposite charge")

    # Compute invariant mass of the dimuon system
    df_mass = df_os.Define(
        "Dimuon_mass",
        "ROOT::VecOps::InvariantMass(Muon_pt, Muon_eta, Muon_phi, Muon_mass)")

    # Book histogram of dimuon mass spectrum
    bins = 30000  # Number of bins in the histogram
    low = 0.25  # Lower edge of the histogram
    up = 300.0  # Upper edge of the histogram

    hist = df_mass.Histo1D(ROOT.RDF.TH1DModel(
        "", "", bins, low, up), "Dimuon_mass")

    # Create canvas for plotting
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "", 800, 700)
    c.SetLogx()
    c.SetLogy()
 
    hist.GetValue() # triggers the event loop

    # Draw histogram
    hist.GetXaxis().SetTitle("m_{#mu#mu} (GeV)")
    hist.GetXaxis().SetTitleSize(0.04)
    hist.GetYaxis().SetTitle("N_{Events}")
    hist.GetYaxis().SetTitleSize(0.04)
    hist.SetStats(False)
    hist.Draw()

    # Draw labels
    label = ROOT.TLatex()
    label.SetTextAlign(22)
    label.DrawLatex(0.55, 3.0e4, "#eta")
    label.DrawLatex(0.77, 7.0e4, "#rho,#omega")
    label.DrawLatex(1.20, 4.0e4, "#phi")
    label.DrawLatex(4.40, 1.0e5, "J/#psi")
    label.DrawLatex(4.60, 1.0e4, "#psi'")
    label.DrawLatex(12.0, 2.0e4, "Y(1,2,3S)")
    label.DrawLatex(91.0, 1.5e4, "Z")
    label.SetNDC(True)
    label.SetTextAlign(11)
    label.SetTextSize(0.04)
    label.DrawLatex(0.10, 0.92, "#bf{CMS Open Data}")
    label.SetTextAlign(31)
    label.DrawLatex(0.90, 0.92, "#sqrt{s} = 8 TeV, L_{int} = 11.6 fb^{-1}")

    # Save Canvas to image
    elapsed = watch.RealTime()
    c.SaveAs("dimuonSpectrum.png")

if __name__ == '__main__':
    filelist =["f1.root", "f2.root", "f3.root", "f4.root"]
    df = RDataFrame("Events", filelist, npartitions=(4*args.cores*args.Nodes), daskclient=client)

    dimuonSpectrum(df)

