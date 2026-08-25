import React, { useMemo } from 'react';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Empresa } from '@/types/empresa';
import { cn } from '@/lib/utils';
import EmpresaCard from './EmpresaCard';

interface EmpresasCardViewProps {
  empresas: Empresa[];
  loading?: boolean;
  currentPage: number;
  itemsPerPage: number;
  onPageChange: (page: number) => void;
  onViewDetails: (empresa: Empresa) => void;
  onViewAnalysis: (empresa: Empresa) => void;
}

const EmpresasCardView: React.FC<EmpresasCardViewProps> = ({
  empresas,
  loading,
  currentPage,
  itemsPerPage,
  onPageChange,
  onViewDetails,
  onViewAnalysis,
}) => {

  const paginatedEmpresas = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return empresas.slice(startIndex, startIndex + itemsPerPage);
  }, [empresas, currentPage, itemsPerPage]);

  const totalPages = Math.ceil(empresas.length / itemsPerPage);

  if (loading) {
    return (
      <div className="flex justify-center items-center p-10">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-4 text-lg text-gray-600">Carregando empresas...</span>
      </div>
    );
  }

  if (empresas.length === 0) {
    return (
      <div className="text-center p-10">
        <h3 className="text-lg font-semibold text-gray-800">Nenhuma empresa encontrada</h3>
        <p className="text-gray-500 mt-2">Tente ajustar seus filtros para encontrar mais resultados.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 w-full">
      <div
        className={cn(
          "grid gap-6 p-4 w-full",
          "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 2xl:grid-cols-4"
        )}
      >
        {paginatedEmpresas.map((empresa) => (
          <EmpresaCard
            key={empresa.cnpj}
            empresa={empresa}
            onViewDetails={onViewDetails}
            onViewAnalysis={onViewAnalysis}
          />
        ))}
      </div>

      {/* Paginação */}
      <div className="bg-white px-4 py-3 border-t border-gray-200 flex items-center justify-between">
        <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p className="text-sm text-gray-700">
              Mostrando{' '}
              <span className="font-medium">{(currentPage - 1) * itemsPerPage + 1}</span> a{' '}
              <span className="font-medium">{Math.min(currentPage * itemsPerPage, empresas.length)}</span> de{' '}
              <span className="font-medium">{empresas.length}</span> resultados
            </p>
          </div>
          <div>
            <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
              <Button
                variant="outline"
                size="sm"
                disabled={currentPage === 1}
                onClick={() => onPageChange(currentPage - 1)}
                className="rounded-r-none"
              >
                Anterior
              </Button>
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                const pageNum = i + 1;
                return (
                  <Button
                    key={pageNum}
                    variant={currentPage === pageNum ? "default" : "outline"}
                    size="sm"
                    onClick={() => onPageChange(pageNum)}
                    className="rounded-none"
                  >
                    {pageNum}
                  </Button>
                );
              })}
              <Button
                variant="outline"
                size="sm"
                disabled={currentPage === totalPages}
                onClick={() => onPageChange(currentPage + 1)}
                className="rounded-l-none"
              >
                Próximo
              </Button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmpresasCardView; 