import Navbar from "../components/layout/Navbar";
import Hero from "../components/hero/Hero";
import DatasetExplorer from "../components/dataset/DatasetExplorer";
import Features from "../components/hero/Features";
import Footer from "../components/layout/Footer";

function Home() {
  return (
    <>
      <Navbar />
      <Hero />
      <DatasetExplorer />
      <Features />
      <Footer />
    </>
  );
}

export default Home;