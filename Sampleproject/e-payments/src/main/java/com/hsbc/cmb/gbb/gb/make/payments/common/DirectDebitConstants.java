import com.fasterxml.jackson.annotation.";

import com.hsbc.cmb.gbb.gb.commons.model.AIMException;

import java.util.HashMap;

import java.util.List;

import java.util.Map;

Created by 45041327 on 3/27/2019.

@JsonInclude(JsonInclude.Include.NON_NULL)

@sonPropertyOrder({

"beneficiaryList", "beneficiary Total",

"pagination",

"alMException"

public class BacsPayeeListMuleResp (

@JsonProperty("aIMException") private List<AIMException> aIMException = null;

@sonProperty("beneficiaryList") private List<BeneficiaryList> beneficiaryList = null;

@3sonProperty("beneficiaryTotal")

private Integer beneficiaryTotal;

@sonProperty("_pagination") private Pagination pagination;

@sonIgnore

private transient Map<String, Object> additional Properties new HashMap();

@JsonProperty("aIMException")

public List<AIMException> getAIMException() { return aIMException;

                                            }
@JsonProperty("aIMException")

public void setAIMException(List<AIMException> aIMException) { this.aIMException aIMException;

}

It will return the beneficiary list

@return

@sonProperty("beneficiaryList")

public List<BeneficiaryList> getBeneficiaryList() { return beneficiaryList;

It will set the beneficiary list coming from

mule api

@param beneficiarylist

@JsonProperty("beneficiaryList")

public void setBeneficiaryList(List<BeneficiaryList> beneficiarylist) ( this.beneficiaryList beneficiaryList;

}

It will get the beneficiary total from

mule api

@return

@JsonProperty("beneficiaryTotal") public Integer getBeneficiaryTotal() {

return beneficiaryTotal;

}

It will set the beneficiary total

@param beneficiary Total

@JsonProperty("beneficiaryTotal")

public void setBeneficiaryTotal (Integer beneficiaryTotal) { this.beneficiaryTotal beneficiary Total;

}

/** It will get the pagination that is show the

page number

@return

@JsonProperty("beneficiaryTotal")

public Integer getBeneficiary Total() {

return beneficiary Total;

}

/**

It will set the beneficiary total

@param beneficiaryTotal

@JsonProperty("beneficiaryTotal")

public void setBeneficiaryTotal (Integer beneficiaryTotal) { this.beneficiaryTotal beneficiary Total;

}

/**

It will get the pagination that is show the

page number

* @return

*/

@JsonProperty("_pagination")

public Pagination getPagination() {

return pagination;

}

It will set the pagination

@param pagination

*/

@JsonProperty("_pagination")

public void setPagination (Pagination pagination) { this.pagination = pagination;

}

@JsonAnyGetter

public Map<String, Object> getAdditional Properties() {

return this.additional Properties;

}

@JsonAnySetter

public void setAdditional Property(String name, Object value) { this.additional Properties.put(name, value);

}

Type here to search

  }
