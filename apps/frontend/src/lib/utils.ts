export function toggleDarkMode() {
  document.documentElement.classList.toggle("prime-dark-mode");
}

export function formatLocalDate(date: Date) {
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, "0");
  const dd = String(date.getDate()).padStart(2, "0");

  return `${yyyy}-${mm}-${dd}`;
}

export const formatPLN = (v: number) =>
  new Intl.NumberFormat("pl-PL", {
    style: "currency",
    currency: "PLN",
  }).format(v);

export function emptyToNull(value?: string | null | undefined) {
  return value === "" ? null : value;
}

export function roundTo2(value: number): number {
  return Math.round(value * 100) / 100;
}

export function calculateGrossPrice(netPrice: number, taxRate: number): number {
  return roundTo2(netPrice * (1 + taxRate));
}

export function calculateNetPrice(grossPrice: number, taxRate: number): number {
  return roundTo2(grossPrice / (1 + taxRate));
}

export function calculateGrossTotal(netPrice: number, amount: number, taxRate: number): number {
  return roundTo2(netPrice * amount * (1 + taxRate));
}

export function calculateNetTotal(netPrice: number, amount: number): number {
  return roundTo2(netPrice * amount);
}

export function calculateTaxTotal(netPrice: number, taxRate: number, amount: number): number {
  return roundTo2(netPrice * taxRate * amount);
}

export function verifyNetVsGrossPrice(
  netPrice: number | null,
  grossPrice: number | null,
  taxRate: number | null,
) {
  if (!netPrice || !grossPrice || !taxRate) return true;
  else
    return (
      netPrice === calculateNetPrice(grossPrice, taxRate) &&
      grossPrice === calculateGrossPrice(netPrice, taxRate)
    );
}
