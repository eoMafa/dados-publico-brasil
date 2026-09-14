import { useState, useEffect } from "react";

interface PontoIndicador {
    data: string;
    valor: number;
}

interface IndicadorCardProps {
    endpoint: string;
    titulo: string;
    cor: string;
}

function IndicadorCard({ endpoint, titulo, cor }: IndicadorCardProps) {
    const [pontos, setPontos] = useState<PontoIndicador[]>([]);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState<string | null>(null);

    useEffect(() => {
        setCarregando(true);
        setErro(null);

        fetch(`${import.meta.env.VITE_API_URL}/${endpoint}?ultimos_n=5`)
            .then((resposta) => {
                if(!resposta.ok){
                    throw new Error("Não foi possível carregar os dados");
                }
                return resposta.json();
            })
            .then((dados) => setPontos(dados))
            .catch((erro) => setErro(erro.message))
            .finally(() => setCarregando(false));
    }, [endpoint]);

    if (carregando) {
        return <p className="text-gray-500 text-sm">Carregando {titulo}...</p>;
    }

    if (erro) {
        return <p className="text-red-500 text-sm">Erro ao carregar {titulo}: {erro}</p>;
    }

    return (
        <div className="bg-white rounded-lg shadow p-4 border-t-4" style={{ borderTopColor: cor }}>
            <h2 className="text-lg font-semibold text-gray-800 mb-2">{titulo}</h2>
            <ul className="space-y-1">
                {pontos.map((ponto) => (
                    <li key={ponto.data} className="flex justify-between text-sm text-gray-600">
                        <span>{ponto.data}</span>
                        <span className="font-medium text-gray-900">{ponto.valor}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default IndicadorCard;