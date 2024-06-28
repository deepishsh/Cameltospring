import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
        "beneficiaryList", "beneficiaryTotal", "pagination", "aIMException"
})
public class BacsPayeeListMuleResp {

    @JsonProperty("aIMException")
    private List<AIMException> aIMException = null;

    @JsonProperty("beneficiaryList")
    private List<BeneficiaryList> beneficiaryList = null;

    @JsonProperty("beneficiaryTotal")
    private Integer beneficiaryTotal;

    @JsonProperty("_pagination")
    private Pagination pagination;

    // Ignore additional properties not bound to specific fields
    private transient Map<String, Object> additionalProperties = new HashMap<>();

    @JsonProperty("aIMException")
    public List<AIMException> getAIMException() {
        return aIMException;
    }

    @JsonProperty("aIMException")
    public void setAIMException(List<AIMException> aIMException) {
        this.aIMException = aIMException;
    }

    @JsonProperty("beneficiaryList")
    public List<BeneficiaryList> getBeneficiaryList() {
        return beneficiaryList;
    }

    @JsonProperty("beneficiaryList")
    public void setBeneficiaryList(List<BeneficiaryList> beneficiaryList) {
        this.beneficiaryList = beneficiaryList;
    }

    @JsonProperty("beneficiaryTotal")
    public Integer getBeneficiaryTotal() {
        return beneficiaryTotal;
    }

    @JsonProperty("beneficiaryTotal")
    public void setBeneficiaryTotal(Integer beneficiaryTotal) {
        this.beneficiaryTotal = beneficiaryTotal;
    }

    @JsonProperty("_pagination")
    public Pagination getPagination() {
        return pagination;
    }

    @JsonProperty("_pagination")
    public void setPagination(Pagination pagination) {
        this.pagination = pagination;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
    }
}
