import {useState} from "react";

interface Feriado {
    date: string | null;
    name: string | null;
    type: string | null;
    weekday: string | null;
}

function BuscaFeriado() {
    const [ano, setAno] = useState("");
    const [feriado, setFeriado] = useState<Feriado[]>([]);
    const [carregando, setCarregando] = useState(false);
    const [erro, setErro] = useState<string | null>(null);

    function buscarFeriado() {
        setCarregando(true);
        setErro(null);
        setFeriado([]);

        fetch(`http://localhost:8000/feriados/${ano}`)
            .then((resposta) => {
                if(!resposta.ok) {
                    throw new Error("Ano inválido ou não encontrado");
                }
                return resposta.json();
            })
            .then((dados) => setFeriado(dados))
            .catch((erro) => setErro(erro.message))
            .finally(() => setCarregando(false));
    }

    return (
        <div className="bg-white rounded-lg shadow p-4">
            <h2 className="text-lg font-semibold text-gray-800 mb-3">Buscar Feriados</h2>
            <div className="flex gap-2">
                <input
                    type="number"
                    value={ano}
                    onChange={(evento) => setAno(evento.target.value)}
                    placeholder="Digite o ano"
                    className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
                <button onClick={buscarFeriado} className="bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-blue-700">Buscar</button>
            </div>
            
            {carregando && <p className="text-gray-500 text-sm mt-3">Carregando...</p>}
            {erro && <p className="text-red-500 text-sm mt-3">Erro: {erro}</p>}
            {feriado.map((f) => (
                <p key={f.date} className="text-gray-700 text-sm mt-3">{f.name} - {f.weekday} - {formatarData(f.date)} - {f.type}</p>
            ))}
            </div>
    )
}

function formatarData(data: string | null): string {
    if (!data) return "";

    const [ano, mes, dia] = data.split("-");
    return `${dia}/${mes}/${ano}`;
}

export default BuscaFeriado;