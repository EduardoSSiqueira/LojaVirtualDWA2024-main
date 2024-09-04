from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from dtos.id_produto_dto import ExcluirProdutoDTO
from dtos.inserir_produto_dto import InserirProdutoDTO
from dtos.problem_detail_dto import ProblemDetailsDto
from models.produto_model import Produto
from repositories.produto_repo import ProdutoRepo
from dtos.alterar_produto_dto import AlterarProdutoDto

router = APIRouter(prefix="/manager")


@router.get("/obter_produtos")
async def obter_produtos():
    produtos = ProdutoRepo.obter_todos()
    return produtos

@router.post("/inserir_produto")
async def inserir_produto(inputDto: InserirProdutoDTO)-> Produto:
    novo_produto = Produto(None, inputDto.nome, inputDto.preco, inputDto.descricao, inputDto.estoque)
    novo_produto=ProdutoRepo.inserir(novo_produto)
    return novo_produto

@router.post("/excluir_produto")
async def excluir_produto(inputDto: ExcluirProdutoDTO) -> bool:
    if ProdutoRepo.excluir(inputDto.id_produto): return None
    pb = ProblemDetailsDto("int", f"O produto com id{inputDto.id_produto} não foi encontrado." , "value_not_found", ["body", "id_produto"])
    return JSONResponse(pb.to_dict(), status_code=404)

@router.post("/alterar_produto")
async def alterar_produto(inputDto: AlterarProdutoDto):
    produto = Produto(inputDto.id, inputDto.nome, inputDto.preco, inputDto.descricao, inputDto.estoque)
    if ProdutoRepo.alterar(produto): return None
    pb = ProblemDetailsDto("int", f"O produto com id <b>{inputDto.id_produto} não foi encontrado." , "value_not_found", ["body", "id_produto"])
    return JSONResponse(pb.to_dict(), status_code=404)