import {useState} from "react";

interface Endereco {
    cep: string | null;
    state: string | null;
    city: string | null;
    neighborhood: string | null;
    street: string | null;
    ibge_cidade: string | null;
    ibge_uf: string | null;
}

function BuscaCep() {
    const [cep, setCep] = useState("");
    const [endereco, setEndereco] = useState<Endereco | null>(null);
    const [carregando, setCarregando] = useState(false);
    const [erro, setErro] = useState<string | null>(null);

    function buscarCep() {
        setCarregando(true);
        setErro(null);
        setEndereco(null);

        fetch(`http://localhost:8000/cep/${cep}`)
            .then((resposta) => {
                if(!resposta.ok) {
                    throw new Error("CEP inválido ou não encontrado");
                }
                return resposta.json();
            })
            .then((dados) => setEndereco(dados))
            .catch((erro) => setErro(erro.message))
            .finally(() => setCarregando(false));
    }

    return (
        <div className="bg-white rounded-lg shadow p-4">
            <h2 className="text-lg font-semibold text-gray-800 mb-3">Buscar CEP</h2>
            <div className="flex gap-2">
                <input
                    type="text"
                    value={cep}
                    onChange={(evento) => setCep(evento.target.value)}
                    placeholder="Digite o CEP (só números)"
                    className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
                <button onClick={buscarCep} className="bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-blue-700">Buscar</button>
            </div>
            
            {carregando && <p className="text-gray-500 text-sm mt-3">Carregando...</p>}
            {erro && <p className="text-red-500 text-sm mt-3">Erro: {erro}</p>}
            {endereco && (
                <p className="text-gray-700 text-sm mt-3">{endereco.city} - {endereco.state}</p>
            )}
        </div>
    )
}

export default BuscaCep;