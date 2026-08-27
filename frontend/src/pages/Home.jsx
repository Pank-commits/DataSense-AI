import Navbar from "../components/layout/Navbar";
import Hero from "../components/hero/Hero";
import DatasetExplorer from "../components/dataset/DatasetExplorer";
import Features from "../components/hero/Features";

function Home() {
  return (
    <>
      <Navbar />
      <Hero />
      <DatasetExplorer />
      <Features />
    </>
  );
}

export default Home;
