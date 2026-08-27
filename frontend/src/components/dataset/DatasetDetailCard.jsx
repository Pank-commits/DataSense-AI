import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Navbar from "../components/layout/Navbar";

import DatasetHero from "../components/dataset/DatasetHero";
import DatasetStats from "../components/dataset/DatasetStats";
import DatasetDescription from "../components/dataset/DatasetDescription";
import DatasetTags from "../components/dataset/DatasetTags";
import DatasetActions from "../components/dataset/DatasetActions";
import RelatedDatasets from "../components/dataset/RelatedDatasets";

import { getDatasetBySlug } from "../Services/datasetService";

function DatasetDetails() {

    const { slug } = useParams();

    const [dataset, setDataset] = useState(null);

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        fetchDataset();

    }, [slug]);

    const fetchDataset = async () => {

        try {

            setLoading(true);

            const response = await getDatasetBySlug(slug);

            setDataset(response);

        }

        catch (error) {

            console.log(error);

        }

        finally {

            setLoading(false);

        }

    };

    if (loading) {

        return (

            <>
                <Navbar />

                <div className="bg-slate-950 min-h-screen flex justify-center items-center">

                    <h1 className="text-white text-3xl font-bold">

                        Loading Dataset...

                    </h1>

                </div>

            </>

        );

    }

    if (!dataset) {

        return (

            <>
                <Navbar />

                <div className="bg-slate-950 min-h-screen flex justify-center items-center">

                    <h1 className="text-red-500 text-3xl font-bold">

                        Dataset Not Found

                    </h1>

                </div>

            </>

        );

    }

    return (

        <>

            <Navbar />

            <div className="bg-slate-950 min-h-screen pt-28">

                <div className="max-w-7xl mx-auto px-6 py-10">

                    <DatasetHero dataset={dataset} />

                    <DatasetStats dataset={dataset} />

                    <DatasetDescription dataset={dataset} />

                    <DatasetTags dataset={dataset} />

                    <DatasetActions dataset={dataset} />

                    <RelatedDatasets
                        category={dataset.category}
                        currentId={dataset.id}
                    />

                </div>


            </div>

        </>

    );

}

export default DatasetDetails;
